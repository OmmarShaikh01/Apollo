function Compile-QT($filepath) {
    $base_name = (Get-Item $filepath).Basename    
    Invoke-Expression -Command "$root_dir\.venv\Scripts\pyside6-uic.exe -g python -o $root_dir\apollo\layout\$base_name.py $root_dir\apollo\layout\$base_name.ui"
}

$pre_exe_dir = Get-Location
$root_dir = Split-Path -Path $(Split-Path -Path $MyInvocation.MyCommand.Definition -Parent) -Parent 
$root_dir = "$(Split-Path -Path $root_dir -Parent)" 
Set-Location $root_dir
clear

Get-ChildItem -Path "$root_dir\apollo\layout" -File -Filter "*.ui" | Foreach {Compile-QT $_.fullname}

Set-Location $pre_exe_dir