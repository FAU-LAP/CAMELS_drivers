@echo off
set /p "pypiuser=pypi user: "
set /p "pypipw=pypi password: "
@echo on
:parse
IF "%~1"=="" GOTO endparse
cd %~1
python -m build
python -m twine upload dist/nomad* -u%pypiuser% -p%pypipw%
cd ..
SHIFT
GOTO parse
:endparse
set "pypipw="