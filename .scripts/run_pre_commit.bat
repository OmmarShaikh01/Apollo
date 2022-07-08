@echo off

cd %~dp0
cd ..       
set ROOT=%cd%

@REM Generate Resources -------------------------------------------------------
@REM Creates requirement.txt
poetry export -f requirements.txt --output requirements.txt --dev --with-credentials --without-hashes


@REM Compiles Qt Layouts
"%ROOT%\.venv\Scripts\pyside6-uic.exe" -g python -o "%ROOT%\apollo\layout\mainwindow.py" "%ROOT%\apollo\layout\mainwindow.ui"

@REM Reformat Code using Black ------------------------------------------------
"%ROOT%\.venv\Scripts\black.exe" "%ROOT%"
"%ROOT%\.venv\Scripts\pylint.exe" "%ROOT%" --output-format=text:"%ROOT%\tests\linter_output.txt"

@REM Test Code ----------------------------------------------------------------
"%ROOT%\.venv\Scripts\nox.exe" --session production_build testing_benchmarked
