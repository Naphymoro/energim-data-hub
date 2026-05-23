import tkinter as tk
from tkinter import messagebox
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / 'run_energim_alpha.bat'

root = tk.Tk()
root.title('ENERGIM Alpha Workstation')
root.geometry('520x320')

status = tk.StringVar(value='Idle')

header = tk.Label(root, text='ENERGIM Alpha Manual Workstation', font=('Arial', 16, 'bold'))
header.pack(pady=12)

info = tk.Label(root, text='Manual execution only. No automatic crawling.', fg='darkred')
info.pack(pady=4)

status_label = tk.Label(root, textvariable=status)
status_label.pack(pady=6)

def run_pipeline():
    try:
        status.set('Running manual pipeline...')
        subprocess.Popen([str(BATCH)], shell=True)
    except Exception as exc:
        messagebox.showerror('ENERGIM Alpha', str(exc))
        status.set('Failed')

buttons = [
    ('Run Crawler Pipeline', run_pipeline),
    ('Open Evidence Store', lambda: subprocess.Popen(f'explorer "{ROOT / "data" / "master" / "evidence"}"')),
    ('Open Validation Reports', lambda: subprocess.Popen(f'explorer "{ROOT / "data" / "master" / "validation"}"')),
    ('Open Run Logs', lambda: subprocess.Popen(f'explorer "{ROOT / "data" / "master" / "provenance" / "crawler_runs"}"')),
]

for text, command in buttons:
    tk.Button(root, text=text, width=40, command=command).pack(pady=6)

root.mainloop()
