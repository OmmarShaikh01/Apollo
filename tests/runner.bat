@ECHO OFF

set og_dir=%cd%
set a=%1
set b=%2
set pytest_dir=.\result\pytest
set cov_dir=.\result\coverage
set PYTHONPATH=..
cd %~dp0

if "%a%"=="pytest" (
    ..\venv\Scripts\pytest.exe --new-first --rootdir=. --ignore=..\venv --cache-clear -v --color=yes --code-highlight=yes
)

if "%a%"=="pytest-f" (
    ..\venv\Scripts\pytest.exe %b% --new-first --rootdir=. --ignore=..\venv --cache-clear --color=yes --code-highlight=yes
)

if "%a%"=="pytest-v" (
    ..\venv\Scripts\pytest.exe --new-first --rootdir=. --ignore=..\venv --cache-clear -vv --color=yes --code-highlight=yes
)

if "%a%"=="coverage-apollo" (
    ..\venv\Scripts\coverage.exe run --branch --omit=..\venv,..\tests\* --source=..\apollo,. -m pytest --new-first --self-contained-html --rootdir=. --ignore=..\venv --cache-clear -v --color=yes --code-highlight=yes --html=%pytest_dir%/result.html .
    ..\venv\Scripts\coverage.exe report -i --skip-empty
    ..\venv\Scripts\coverage.exe html -i --show-contexts --skip-empty -d %cov_dir%
    ..\venv\Scripts\coverage.exe erase
)

if "%a%"=="coverage-complete" (
    ..\venv\Scripts\coverage.exe run --branch --omit=..\venv --source=..\apollo,. -m pytest --new-first --self-contained-html --rootdir=. --ignore=..\venv --cache-clear -v --color=yes --code-highlight=yes --html=%pytest_dir%/result.html .
    ..\venv\Scripts\coverage.exe report -i --skip-empty
    ..\venv\Scripts\coverage.exe html -i --show-contexts --skip-empty -d %cov_dir%
    ..\venv\Scripts\coverage.exe erase
)

if "%a%"=="pytest-html" (
    ..\venv\Scripts\pytest.exe --new-first --self-contained-html --rootdir=. --ignore=..\venv --cache-clear -v --color=yes --code-highlight=yes --html=%pytest_dir%/result.html
)
PAUSE
cd /d %og_dir%
cls
ECHO ON
