# ENERGIM Apps Script Backend

This folder contains the free Google-native backend for ENERGIM Alpha.

## Purpose

Use Google Apps Script as the lightweight backend between the GitHub Pages policy-maker interface and Google Sheets / Google Drive.

Policy makers should not use terminals, notebooks, or VS Code. They should use the browser interface. Technical operators may still use the Windows workstation for heavy crawling, OCR, SDMX conversion, and LEAP/NEMO export generation.

## Architecture

GitHub Pages UI -> Apps Script Web App -> Google Sheets registry -> Google Drive evidence and outputs -> Windows workstation processing engine.

## What Apps Script does

- Creates evidence run records.
- Lists evidence runs.
- Registers Drive folders and files.
- Stores reviewer approvals and decisions.
- Returns status to the HTML dashboard.
- Links Drive outputs and reports.

## What Apps Script must not do

- It must not run heavy OCR.
- It must not run uncontrolled crawling.
- It must not auto-promote candidate data.
- It must not bypass validation gates.

## Deployment

1. Open script.google.com.
2. Create a new Apps Script project.
3. Copy `Code.gs` into the project.
4. Set script properties for `SPREADSHEET_ID` and optional `DRIVE_ROOT_FOLDER_ID`.
5. Deploy as a Web App.
6. Set access according to your institutional policy.
7. Copy the Web App URL into `alpha/control-center.html` or frontend config.
