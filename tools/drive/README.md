# Google Drive Integration Layer

Purpose:
Index, synchronize, and operationalize institutional evidence stored in Google Drive and Google Sheets.

Planned scripts:

- sync_drive.py
- sync_sheets.py

Expected workflow:

Google Drive file
-> local evidence archive
-> OCR/parser
-> extracted tables
-> normalized candidate values
-> validation gate
-> LEAP/NEMO staging

Important:
Drive evidence is candidate evidence only until validation quorum is satisfied.
