#!/usr/bin/env python3
"""ENERGIM Alpha Crawler Hunt Mode.

Discovers Rwanda energy-system evidence and writes candidate records into
data/master. The crawler never validates or releases model data; it only
creates traceable evidence for the validator workflow.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import html
from html.parser import HTMLParser
import json
import mimetypes
from pathlib import Path
import re
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen


USER_AGENT = "ENERGIM-Alpha-Crawler/0.1 (+https://naphymoro.github.io/energim-data-hub/alpha/)"
TEXT_LIMIT_BYTES = 1_200_000
DEFAULT_TIMEOUT = 20

YEAR_RE = re.compile(r"\b(201[5-9]|202[0-9]|203[0-9]|204[0-9]|2050)\b")
UNIT_RE = re.compile(
    r"\b(ktoe|toe|tj|gj|gwh|mwh|kwh|mw|kw|usd/kwh|usd/kw|usd/mwh|rwf|tco2e/tj|tco2/gwh|m3/s|l/100km|litres|tonnes|kg|%)\b",
    re.IGNORECASE,
)
RELEVANT_EXTENSIONS = {".pdf", ".csv", ".xls", ".xlsx", ".doc", ".docx", ".zip", ".json", ".xml"}
RELEVANT_LINK_WORDS = {
    "annual",
    "report",
    "publication",
    "statistics",
    "data",
    "dataset",
    "energy",
    "electricity",
    "power",
    "generation",
    "capacity",
    "tariff",
    "loss",
    "fuel",
    "biomass",
    "charcoal",
    "cooking",
    "solar",
    "hydro",
    "transport",
    "emission",
    "climate",
    "ndc",
    "inventory",
    "policy",
}

DATASET_RULES = [
    {
        "dataset_id": "RW_ENBAL_TOTAL_2015_2024",
        "category": "National energy balance",
        "legacy_hint": "Stable inventory energy balance and aggregate demand/supply items",
        "leap": "LEAP baseline",
        "nemo": "NEMO fuel balance",
        "keywords": ["energy balance", "final energy", "primary energy", "electricity consumption", "energy statistics", "fuel consumption"],
    },
    {
        "dataset_id": "RW_PWR_GEN_TECH_GWH",
        "category": "Electricity generation",
        "legacy_hint": "Annual electricity generation by plant or technology",
        "leap": "Transformation",
        "nemo": "Technology activity",
        "keywords": ["generation", "generated", "gwh", "dispatch", "power plant", "electricity production"],
    },
    {
        "dataset_id": "RW_PWR_CAP_TECH_MW",
        "category": "Installed capacity",
        "legacy_hint": "Installed generation capacity by plant or technology",
        "leap": "Capacity",
        "nemo": "Existing capacity",
        "keywords": ["installed capacity", "capacity", "mw", "power plant", "commissioning", "generation capacity"],
    },
    {
        "dataset_id": "RW_RES_COOK_FUEL_SHARE",
        "category": "Residential cooking",
        "legacy_hint": "Cooking fuel share, cookstove, LPG, biogas and clean cooking items",
        "leap": "Residential demand",
        "nemo": "Fuel shares",
        "keywords": ["cooking", "cookstove", "cook stove", "lpg", "biogas", "charcoal", "wood fuel", "clean cooking"],
    },
    {
        "dataset_id": "RW_BIOMASS_CHARCOAL_TJ",
        "category": "Biomass and charcoal",
        "legacy_hint": "Biomass, charcoal, woodfuel and forestry resource items",
        "leap": "Biomass demand",
        "nemo": "Fuel constraint",
        "keywords": ["biomass", "charcoal", "woodfuel", "wood fuel", "forestry", "firewood", "pellet", "briquette"],
    },
    {
        "dataset_id": "RW_TRANSPORT_FUEL_TJ",
        "category": "Transport fuels",
        "legacy_hint": "Transport fuel, vehicle fleet, VKT, EV and fuel import items",
        "leap": "Transport demand",
        "nemo": "Demand proxy",
        "keywords": ["transport", "vehicle", "electric vehicle", "fuel import", "petrol", "diesel", "e-mobility", "traffic", "vkt"],
    },
    {
        "dataset_id": "RW_SOCIO_GDP_POP",
        "category": "Socioeconomic drivers",
        "legacy_hint": "Population, GDP, income, urbanization and macro driver items",
        "leap": "Key assumptions",
        "nemo": "Demand driver",
        "keywords": ["population", "gdp", "household", "urban", "income", "census", "eicv", "macroeconomic"],
    },
    {
        "dataset_id": "RW_EF_FUEL_IPCC",
        "category": "Emission factors",
        "legacy_hint": "Fuel emission factor, grid factor and national inventory items",
        "leap": "Environmental loadings",
        "nemo": "Emission factor",
        "keywords": ["emission", "emissions", "co2", "ghg", "greenhouse", "inventory", "ipcc", "ndc", "climate"],
    },
    {
        "dataset_id": "RW_TECH_COSTS",
        "category": "Technology costs",
        "legacy_hint": "CAPEX, OPEX, fuel cost, heat rate and technology-cost items",
        "leap": "Scenario assumptions",
        "nemo": "CAPEX/OPEX",
        "keywords": ["capex", "opex", "cost", "tariff", "ppa", "investment", "heat rate", "fuel cost"],
    },
    {
        "dataset_id": "RW_PROJECT_PIPELINE",
        "category": "Project pipeline",
        "legacy_hint": "Planned generation additions, SHS, mini-grid, pipeline and policy target items",
        "leap": "Scenario additions",
        "nemo": "Candidate technologies",
        "keywords": ["pipeline", "project", "planned", "target", "irp", "mini-grid", "solar home", "developer", "procurement"],
    },
]


class EvidenceHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.text_parts: list[str] = []
        self.title_parts: list[str] = []
        self._in_title = False
        self._current_href: str | None = None
        self._current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag.lower() == "title":
            self._in_title = True
        if tag.lower() == "a" and attrs_dict.get("href"):
            self._current_href = attrs_dict["href"]
            self._current_text = []

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False
        if tag.lower() == "a" and self._current_href:
            label = " ".join("".join(self._current_text).split())
            self.links.append((self._current_href, label))
            self._current_href = None
            self._current_text = []

    def handle_data(self, data: str) -> None:
        cleaned = " ".join(html.unescape(data).split())
        if not cleaned:
            return
        if self._in_title:
            self.title_parts.append(cleaned)
        if self._current_href:
            self._current_text.append(cleaned)
        self.text_parts.append(cleaned)

    @property
    def title(self) -> str:
        return " ".join(self.title_parts).strip()

    @property
    def text(self) -> str:
        return " ".join(self.text_parts)


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")


def fetch(url: str, timeout: int) -> dict[str, Any]:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    try:
        with urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            status = getattr(response, "status", 200)
            final_url = response.geturl()
            body = response.read(TEXT_LIMIT_BYTES + 1)
            truncated = len(body) > TEXT_LIMIT_BYTES
            if truncated:
                body = body[:TEXT_LIMIT_BYTES]
            return {
                "ok": True,
                "status": status,
                "url": final_url,
                "content_type": content_type,
                "body": body,
                "truncated": truncated,
                "error": "",
            }
    except HTTPError as exc:
        return {"ok": False, "status": exc.code, "url": url, "content_type": "", "body": b"", "truncated": False, "error": str(exc)}
    except (URLError, TimeoutError, OSError) as exc:
        return {"ok": False, "status": "", "url": url, "content_type": "", "body": b"", "truncated": False, "error": str(exc)}


def file_type_for(url: str, content_type: str) -> str:
    ext = Path(urlparse(url).path).suffix.lower()
    if ext:
        return ext.lstrip(".")
    if content_type:
        return content_type.split(";")[0].split("/")[-1]
    guessed = mimetypes.guess_type(url)[0]
    return guessed.split("/")[-1] if guessed else "unknown"


def parse_html(body: bytes, url: str) -> tuple[str, str, list[tuple[str, str]]]:
    text = body.decode("utf-8", errors="replace")
    parser = EvidenceHTMLParser()
    parser.feed(text)
    links: list[tuple[str, str]] = []
    for href, label in parser.links:
        full_url = urldefrag(urljoin(url, href))[0]
        if full_url.startswith(("http://", "https://")):
            links.append((full_url, label))
    return parser.title, parser.text, links


def is_same_host(a: str, b: str) -> bool:
    return urlparse(a).netloc.lower() == urlparse(b).netloc.lower()


def relevant_link(url: str, label: str) -> bool:
    path = urlparse(url).path.lower()
    ext = Path(path).suffix.lower()
    if ext in RELEVANT_EXTENSIONS:
        return True
    haystack = f"{path} {label}".lower()
    return any(word in haystack for word in RELEVANT_LINK_WORDS)


def detect_years(text: str) -> list[str]:
    return sorted(set(YEAR_RE.findall(text)))


def detect_units(text: str) -> list[str]:
    return sorted({match.lower() for match in UNIT_RE.findall(text)})


def score_datasets(text: str) -> list[dict[str, Any]]:
    haystack = text.lower()
    matches: list[dict[str, Any]] = []
    for rule in DATASET_RULES:
        score = 0
        for keyword in rule["keywords"]:
            pattern = r"(?<![a-z0-9])" + re.escape(keyword.lower()) + r"(?![a-z0-9])"
            score += len(re.findall(pattern, haystack))
        if score:
            matches.append({**rule, "score": score})
    matches.sort(key=lambda item: (-item["score"], item["dataset_id"]))
    return matches


def confidence_for_tier(tier: str) -> str:
    return {"1": "B", "2": "B", "3": "D", "4": "C", "5": "E"}.get(str(tier), "E")


def evidence_id_for(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def make_evidence_record(source: dict[str, str], discovered_url: str, title: str, text: str, file_type: str, status: Any, error: str = "") -> dict[str, Any]:
    matches = score_datasets(f"{title} {discovered_url} {text[:15000]}")
    mapped = matches[:4]
    dataset_ids = [item["dataset_id"] for item in mapped]
    categories = [item["category"] for item in mapped]
    return {
        "evidence_id": evidence_id_for(discovered_url),
        "source_id": source.get("source_id", ""),
        "source_title": source.get("title", ""),
        "institution": source.get("institution", ""),
        "source_tier": source.get("tier", ""),
        "source_url": source.get("url", ""),
        "discovered_url": discovered_url,
        "title": title or discovered_url,
        "access_date_utc": utc_now(),
        "http_status": status,
        "file_type": file_type,
        "dataset_category": "; ".join(categories),
        "matching_alpha_dataset_ids": "; ".join(dataset_ids),
        "matching_legacy_inventory_item": "; ".join(item["legacy_hint"] for item in mapped),
        "leap_relevance": "; ".join(item["leap"] for item in mapped),
        "nemo_relevance": "; ".join(item["nemo"] for item in mapped),
        "years_detected": "; ".join(detect_years(text)),
        "units_detected": "; ".join(detect_units(text)),
        "extraction_method": "html_text_scan" if file_type in {"html", "htm"} else "metadata_scan",
        "confidence_level": confidence_for_tier(source.get("tier", "")),
        "validation_status": "candidate",
        "validator_quorum_required": "AIMS RIC + 2 approved validators",
        "mandatory_validator": "AIMS RIC",
        "additional_validator_pool": "ENERGIM partners; EPD; WRI; Rwanda public institutions; approved technical experts",
        "reviewer_notes": "Crawler candidate. Not validated for LEAP/NEMO export.",
        "crawler_error": error,
    }


def crawl_source(source: dict[str, str], args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root_url = source["url"]
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    fetched = 0
    queued: list[tuple[str, str, int]] = [(root_url, source.get("title", ""), 0)]
    seen: set[str] = set()
    max_links = int(source.get("max_links") or args.max_links)
    crawl_depth = min(int(source.get("crawl_depth") or 0), args.max_depth)

    while queued and fetched < max_links + 1:
        url, label, depth = queued.pop(0)
        url = urldefrag(url)[0]
        if url in seen:
            continue
        seen.add(url)
        if depth > crawl_depth:
            continue
        time.sleep(args.delay)
        result = fetch(url, args.timeout)
        fetched += 1
        content_type = result["content_type"]
        file_type = file_type_for(result["url"], content_type)

        if not result["ok"]:
            errors.append(f"{url}: {result['error']}")
            records.append(make_evidence_record(source, url, label, "", file_type, result["status"], result["error"]))
            continue

        title = label or result["url"]
        text = ""
        links: list[tuple[str, str]] = []
        if "html" in content_type or file_type in {"html", "htm", "unknown"}:
            title, text, links = parse_html(result["body"], result["url"])
            for link_url, link_label in links:
                if len(queued) >= max_links:
                    break
                if not is_same_host(root_url, link_url):
                    continue
                if relevant_link(link_url, link_label):
                    queued.append((link_url, link_label, depth + 1))
        else:
            text = f"{title} {result['url']}"

        if url == root_url or relevant_link(result["url"], title) or score_datasets(f"{title} {result['url']} {text[:5000]}"):
            records.append(make_evidence_record(source, result["url"], title, text, file_type, result["status"]))

    summary = {
        "source_id": source.get("source_id", ""),
        "url": root_url,
        "fetched": fetched,
        "records": len(records),
        "errors": errors[:10],
    }
    return records, summary


def load_existing_records(path: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return records
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            records[row.get("evidence_id", evidence_id_for(row.get("discovered_url", "")))] = row
    return records


def update_catalog(catalog_path: Path, records: list[dict[str, Any]]) -> None:
    rows = read_csv(catalog_path)
    counts: dict[str, int] = {}
    for record in records:
        for dataset_id in [part.strip() for part in record.get("matching_alpha_dataset_ids", "").split(";") if part.strip()]:
            counts[dataset_id] = counts.get(dataset_id, 0) + 1
    for row in rows:
        row["candidate_evidence_count"] = str(counts.get(row["dataset_id"], 0))
        if row.get("validation_status") not in {"validated", "needs_reconciliation", "under_review"}:
            row["validation_status"] = "candidate" if counts.get(row["dataset_id"], 0) else row.get("validation_status", "candidate")
    write_csv(catalog_path, rows, list(rows[0].keys()))


def write_candidate_csv(path: Path, records: list[dict[str, Any]]) -> None:
    fields = [
        "evidence_id",
        "source_id",
        "institution",
        "source_tier",
        "discovered_url",
        "title",
        "access_date_utc",
        "file_type",
        "dataset_category",
        "matching_alpha_dataset_ids",
        "leap_relevance",
        "nemo_relevance",
        "years_detected",
        "units_detected",
        "confidence_level",
        "validation_status",
        "validator_quorum_required",
        "crawler_error",
    ]
    write_csv(path, records, fields)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run ENERGIM Alpha Crawler Hunt Mode")
    parser.add_argument("--registry", default="data/master/source_registry.csv", help="Source registry CSV")
    parser.add_argument("--out", default="data/master", help="Master data output directory")
    parser.add_argument("--max-sources", type=int, default=999, help="Maximum sources to crawl")
    parser.add_argument("--max-links", type=int, default=30, help="Maximum discovered links per source")
    parser.add_argument("--max-depth", type=int, default=1, help="Maximum same-host link depth")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Fetch timeout in seconds")
    parser.add_argument("--delay", type=float, default=0.35, help="Delay between fetches per source")
    parser.add_argument("--reset-output", action="store_true", help="Replace existing evidence outputs instead of merging")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    registry_path = Path(args.registry)
    out_dir = Path(args.out)
    evidence_path = out_dir / "evidence_records.jsonl"
    candidate_csv_path = out_dir / "candidate_evidence.csv"
    run_log_path = out_dir / "crawler_runs.jsonl"
    latest_summary_path = out_dir / "metadata" / "crawler_latest_summary.json"
    catalog_path = out_dir / "data_catalog.csv"

    sources = read_csv(registry_path)[: args.max_sources]
    existing = {} if args.reset_output else load_existing_records(evidence_path)
    all_records = dict(existing)
    run_summaries: list[dict[str, Any]] = []
    started = utc_now()

    for source in sources:
        records, summary = crawl_source(source, args)
        run_summaries.append(summary)
        for record in records:
            all_records[record["evidence_id"]] = record

    merged_records = sorted(all_records.values(), key=lambda row: (row.get("source_id", ""), row.get("title", "")))
    write_jsonl(evidence_path, merged_records)
    write_candidate_csv(candidate_csv_path, merged_records)
    if catalog_path.exists():
        update_catalog(catalog_path, merged_records)

    run_record = {
        "run_id": hashlib.sha256(f"{started}-{len(run_summaries)}".encode("utf-8")).hexdigest()[:12],
        "started_utc": started,
        "finished_utc": utc_now(),
        "source_count": len(sources),
        "evidence_record_count": len(merged_records),
        "new_or_updated_records_this_run": sum(item["records"] for item in run_summaries),
        "summaries": run_summaries,
    }
    append_jsonl(run_log_path, [run_record])
    latest_summary_path.parent.mkdir(parents=True, exist_ok=True)
    latest_summary_path.write_text(json.dumps(run_record, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(run_record, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
