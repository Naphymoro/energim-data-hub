@echo off
setlocal
set RUN_ID=RUN_%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
set RUN_ID=%RUN_ID: =0%
set LOG_DIR=data\master\provenance\crawler_runs\%RUN_ID%
mkdir "%LOG_DIR%"
echo ENERGIM Alpha manual workstation run > "%LOG_DIR%\console.log"
echo Run ID: %RUN_ID% >> "%LOG_DIR%\console.log"
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
echo Running governed pipeline...
python tools\crawler\run_evidence_harvest.py >> "%LOG_DIR%\console.log" 2>> "%LOG_DIR%\errors.log"
python tools\crawler\extract_payloads.py >> "%LOG_DIR%\console.log" 2>> "%LOG_DIR%\errors.log"
python tools\crawler\build_normalized_candidates.py >> "%LOG_DIR%\console.log" 2>> "%LOG_DIR%\errors.log"
python tools\sdmx\build_sdmx_candidates.py >> "%LOG_DIR%\console.log" 2>> "%LOG_DIR%\errors.log"
python tools\sdmx\sdmx_gate.py >> "%LOG_DIR%\console.log" 2>> "%LOG_DIR%\errors.log"
python tools\exports\export_leap_ready.py >> "%LOG_DIR%\console.log" 2>> "%LOG_DIR%\errors.log"
python tools\exports\export_nemo_ready.py >> "%LOG_DIR%\console.log" 2>> "%LOG_DIR%\errors.log"
echo Completed. Logs stored in %LOG_DIR%
pause
