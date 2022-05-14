CLS
@echo off

SETLOCAL
SET "__NAME=%~n0"
SET "__VERSION=1.0"
SET "__YEAR=2017"

SET "__BAT_FILE=%~0"
SET "__BAT_PATH=%~dp0"
SET "__BAT_NAME=%~nx0"

SET "OptHelp="
SET "OptVersion="
SET "OptVerbose="
SET "VENV=.\.venv"
goto :parse

:header
    echo. ----------------------------------------
    echo. A Simple Script to build and test apollo
    echo. ----------------------------------------
    goto :eof

:usage
    echo. Usage: %__BAT_PATH%%__BAT_NAME% [options] [required flags]
    echo.
    echo. Options:
    echo.     -?, --help                    Displays help on commandline options.
    echo.     -v, --version                 Displays version information.
    echo.     -e, --verbose                 Displays Verbose information.
    echo. Required Flags:
    echo.     --pytest                      Runs Pytest
    echo.     --pytest --id path_id         Runs Pytest for the path matching the id
    echo.     --cov-pytest                  Runs Pytest with coverage
    echo.     --cov-pytest --id path_id     Runs Pytest with coverage for the path matching the id
    echo.     --sphinx-build                Runs Sphinx builds the document
    echo.     --qt-compile                  Runs Compiles the UI layouts
    goto :eof

:version
    echo. Version: 1.0
    goto :eof

:parse
    if /i "%~1"==""           call :header & call :usage & goto :end

    if /i "%~1"=="-?"         call :header & call :usage & goto :end
    if /i "%~1"=="--help"     call :header & call :usage & goto :end

    if /i "%~1"=="-v"         call :version      & goto :end
    if /i "%~1"=="--version"  call :version      & goto :end

    if /i "%~1"=="-e"         set "OptVerbose=yes"  & shift & goto :parse
    if /i "%~1"=="--verbose"  set "OptVerbose=yes"  & shift & goto :parse

    if /i "%~1"=="--pytest"         goto :pytest
    if /i "%~1"=="--cov-pytest"     goto :coverage pytest
    if /i "%~1"=="--sphinx-build"   goto :sphinx build doc
    if /i "%~1"=="--qt-compile"     goto :qt compile

    shift
    goto :parse

:end
    exit /B

:pytest
    ECHO started pytest
    shift
    if /i "%~1"=="--id" set class_id=.\tests\pytest\%~2

    if defined OptVerbose (
        echo **** DEBUG IS ON
        %VENV%\Scripts\pytest.exe --rootdir=.\tests\pytest -c .\pytest.ini -vv %class_id%
    ) ELSE (
        %VENV%\Scripts\pytest.exe -ra -q --rootdir=.\tests\pytest -c .\pytest.ini %class_id%
    )
    GOTO :eof

:coverage pytest
    ECHO started coverage_py
    shift
    if /i "%~1"=="--id" set class_id=.\tests\pytest\%~2
    if defined OptVerbose (
        echo **** DEBUG IS ON
        %VENV%\Scripts\pytest.exe --cov=.\apollo --rootdir=.\tests\pytest --cov-config=.coveragerc  -c pytest.ini  --cov-report=html -vv
    ) ELSE (
        %VENV%\Scripts\pytest.exe -ra -q --cov=.\apollo --rootdir=.\tests\pytest --cov-config=.coveragerc  -c pytest.ini  --cov-report=html
    )
    ECHO BUILD COVERAGE REPORT INTO [%__BAT_PATH%tests\pytest\coverage]
    ECHO COVERAGE REPORT %__BAT_PATH%tests\coverage\html\index.html
    start "" %__BAT_PATH%tests\coverage\html\index.html


    GOTO :eof

:sphinx build doc
    ECHO started sphinx_build
    %VENV%\Scripts\sphinx-apidoc.exe -f -e -M -o .\docs\source\ .\apollo
    %VENV%\Scripts\sphinx-build.exe -b html .\docs\source .\docs\build
    ECHO BUILD SPHINX DOCS INTO [%__BAT_PATH%docs\build]
    ECHO SPHINX DOCS %__BAT_PATH%docs\build\index.html
    start "" %__BAT_PATH%docs\build\index.html
    GOTO :eof

:qt compile
    ECHO started qt_compile
    %VENV%\Scripts\pyside6-uic.exe -g python -o .\apollo\layout\ui_mainwindow.py .\apollo\layout\mainwindow.ui
    ECHO COMPILED [%__BAT_PATH%apollo\layout\mainwindow.ui] TO [%__BAT_PATH%apollo\layout\ui_mainwindow.py]
    GOTO :eof

ENDLOCAL
