@echo off

cd "src"
pipenv run cxfreeze -c main_server.py --target-dir ../../Dynatrace_Config_Manager-win64/app --target-name Dynatrace_Config_Manager-win64 --icon favicon.ico
cd ..