<#
.SYNOPSIS
    Helper script to build Apollo
.DESCRIPTION
    This script will detect Python installation, and build Apolllo to `build`
    directory using existing virtual environment created by poetry -q. It will 
    then detect dependencies in project folder to optimize for different Python.
.EXAMPLE
    PS> .\build.ps1
#>

clear

$art = @"
  ___              _ _       
 / _ \            | | |      
/ /_\ \_ __   ___ | | | ___  
|  _  | '_ \ / _ \| | |/ _ \ 
| | | | |_) | (_) | | | (_) |
\_| |_/ .__/ \___/|_|_|\___/ 
      | |                    
      |_|  Made By Ommar Shaikh                  

"@
Write-Host $art -ForegroundColor Green
$pre_exe_dir = Get-Location
$root_dir = Split-Path -Path $(Split-Path -Path $MyInvocation.MyCommand.Definition -Parent) -Parent 
Set-Location $root_dir


function Exit-WithCode($exitcode) {
   # Only exit this host process if it's a child of another PowerShell parent process...
   $parentPID = (Get-CimInstance -ClassName Win32_Process -Filter "ProcessId=$PID" | Select-Object -Property ParentProcessId).ParentProcessId
   $parentProcName = (Get-CimInstance -ClassName Win32_Process -Filter "ProcessId=$parentPID" | Select-Object -Property Name).Name
   if ('powershell.exe' -eq $parentProcName) { $host.SetShouldExit($exitcode) }
   Set-Location $pre_exe_dir
   exit $exitcode
}


function Startup-Tasks() {
    Write-Host ">>> " -NoNewline -ForegroundColor Green
    Write-Host "Reading poetry ... " -NoNewline
    if (-not (Get-Command "poetry.exe" -ErrorAction SilentlyContinue)) {
        Write-Host "NOT FOUND" -ForegroundColor Yellow
        Write-Host "*** " -NoNewline -ForegroundColor Yellow
        Write-Host "We need to install poetry and create virtual env first ..."   
        Exit-WithCode 1 
    } else {
        Write-Host "OK" -ForegroundColor Green        
    }
    Write-Host 
}


function Lint-Apollo() {
    Write-Host ">>> " -NoNewline -ForegroundColor Green
    Write-Host "Isort Reformat... " 
    poetry -q run isort -q .
    Write-Host

    Write-Host ">>> " -NoNewline -ForegroundColor Green
    Write-Host "Black Reformat... " 
    poetry -q run black -q .
    Write-Host
}


function Build-Apollo() {
    Write-Host ">>> " -NoNewline -ForegroundColor Green
    Write-Host "Cleaning build directory ..."
    if (-not (Test-Path -Path "$($root_dir)\dist" -PathType Container)) {
        New-Item -ItemType Directory -Force -Path "$($root_dir)\dist" | Out-Null
    } else {
        try {
            Remove-Item -Recurse -Force "$($root_dir)\dist\*"
        } catch {
            Write-Host "!!! " -NoNewline -ForegroundColor Red
            Write-Host "Cannot clean build directory, possibly because process is using it."
            Write-Host $_.Exception.Message
            Exit-WithCode 1
        }      
    }   
    Write-Host         

    Write-Host ">>> " -NoNewline -ForegroundColor Green
    Write-Host "poetry Build Dist ..."
    poetry build -f sdist     
    Write-Host   
}


function Freeze-Apollo {
    $dist_zip = @(Get-ChildItem -Path "$($root_dir)\dist\*" -Include *.tar.gz)[0]
    if (Test-Path -Path $dist_zip -PathType Leaf) {
        Write-Host ">>> " -NoNewline -ForegroundColor Green
        Write-Host "Extracting Build Dist ..."
        tar -xzf $dist_zip -C "$($root_dir)\dist"
        Set-Location @(Get-ChildItem -Path "$($root_dir)\dist" -Exclude *.tar.gz)[0]
        Write-Host

        Write-Host ">>> " -NoNewline -ForegroundColor Green
        Write-Host "Pyinstaller Freeze Dist ..."
        poetry install --no-root > "$($root_dir)\dist\build_dep.log"
        New-Item -ItemType Directory -Force -Path "$($root_dir)\dist\build" | Out-Null
        poetry run python build.py > "$($root_dir)\dist\build.log"        
        Write-Host
    } else {
        Write-Host "!!! " -NoNewline -ForegroundColor Red
        Write-Host "Cannot Find Dist Zip"    
        Exit-WithCode 1    
    }

    Write-Host ">>> " -NoNewline -ForegroundColor Green
    Write-Host "Apollo Build Successful"
    Move-Item -Force "$(@(Get-ChildItem -Path "$($root_dir)\dist" -Exclude *.tar.gz)[0])\dist\Apollo" -Destination "$($root_dir)\dist\build"
    Copy-Item -Force "$($root_dir)\tools\installer.nsi" -Destination "$($root_dir)\dist\build\installer.nsi"
    Write-Host 

    Write-Host ">>> " -NoNewline -ForegroundColor Green
    Write-Host "Cleaning build directory ..."
    if (Test-Path -Path "$($root_dir)\dist" -PathType Container) {           
        try {
            Remove-Item -Recurse -Force @(Get-ChildItem -Path "$($root_dir)\dist\*" -Include *.tar.gz)[0]            
            # ENABLE IN PRODUCTION
            Remove-Item -Recurse -Force "$(@(Get-ChildItem -Path "$($root_dir)\dist\" -Attributes Directory -Exclude *build)[0])\dist"          
        } catch {
            Write-Host "!!! " -NoNewline -ForegroundColor Red
            Write-Host "Cannot clean build directory, possibly because process is using it."
            Write-Host "!!! " -NoNewline -ForegroundColor Red
            Write-Host $_.Exception.Message
            Exit-WithCode 1
        }      
    }   
    Write-Host   
    
    $apollo = "$($root_dir)\dist\build\Apollo"
    Write-Host ">>> " -NoNewline -ForegroundColor Green
    Write-Host "Compressing Apollo"
    if (Test-Path -Path $apollo -PathType Container) {
        Compress-Archive -LiteralPath $apollo -DestinationPath "$($apollo).zip" -Force -CompressionLevel "Optimal"       
    } else {
        Write-Host "!!! " -NoNewline -ForegroundColor Red
        Write-Host "Failed to Compress Apollo"
    }  
    Write-Host   
}


function NSIS-Apollo {
    $build = "$($root_dir)\dist\build\"

    Write-Host ">>> " -NoNewline -ForegroundColor Green
    Write-Host "NSIS Compile Apollo.exe ... " 
    Write-Host 

    Write-Host ">>> " -NoNewline -ForegroundColor Green
    Write-Host "Checking makensis ... " -NoNewline
    if (-not (Get-Command "makensis.exe" -ErrorAction SilentlyContinue)) {
        Write-Host "NOT FOUND" -ForegroundColor Yellow
        Write-Host "*** " -NoNewline -ForegroundColor Yellow
        Write-Host "We need to install makensis and add it to env first ..."   
        Exit-WithCode 1 
    } else {
        Write-Host "OK" -ForegroundColor Green        
    }
    Write-Host 

    Write-Host ">>> " -NoNewline -ForegroundColor Green
    Write-Host "Compiling Apollo.exe ... " 
    makensis /P5 /V2 "$($build)\installer.nsi"
    Write-Host     

    Move-Item -Force "$($root_dir)\dist\build\Apollo.exe" -Destination "$($root_dir)\dist\Apollo.exe"
    Set-Location $root_dir
    Remove-Item "$($root_dir)\dist" -Exclude *.exe -Recurse -Force
}


function Main {

    Write-Host ">>> " -NoNewline -ForegroundColor Green
    Write-Host "Building Apollo ... " 
    Write-Host 

    Startup-Tasks
    Lint-Apollo
    Build-Apollo
    Freeze-Apollo
    NSIS-Apollo   

    Set-Location $pre_exe_dir
}


# Execute Script --------------------------------------------------------------
"Time Elapsed: $(
    $(
        Measure-Command {Main} |
        Select-Object {"$($_.Minutes) Minutes $($_.Seconds) Seconds $($_.Milliseconds) Milliseconds"} |
        Out-String -Stream |
        Select-String -Pattern '\d+\w+' |
        Out-String
    ).Trim()
)"