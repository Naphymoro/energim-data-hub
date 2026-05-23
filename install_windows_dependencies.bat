@echo off
echo ENERGIM Alpha Windows environment check
python --version > environment_check_report.txt 2>&1
pip --version >> environment_check_report.txt 2>&1
where tesseract >> environment_check_report.txt 2>&1
where java >> environment_check_report.txt 2>&1
where gswin64c >> environment_check_report.txt 2>&1
echo Creating required folders... >> environment_check_report.txt
mkdir data\master\evidence\raw\html 2>nul
mkdir data\master\evidence\raw\pdf 2>nul
mkdir data\master\evidence\extracted\tables 2>nul
mkdir data\master\evidence\extracted\normalized_candidates 2>nul
mkdir data\master\model_inputs\leap_ready 2>nul
mkdir data\master\model_inputs\nemo_ready 2>nul
echo Environment check complete. Review environment_check_report.txt
pause
