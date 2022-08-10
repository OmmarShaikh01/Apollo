# Includes ---------------------------------
!include MUI2.nsh
!define APPNAME Apollo
Var STARTMENUFOLDER


# Settings ---------------------------------
Name ${APPNAME}
OutFile ${__FILEDIR__}\${APPNAME}.exe
InstallDir $PROGRAMFILES\${APPNAME}
InstallDirRegKey HKCU "Software\Apollo" "Installdir"
LicenseData ${__FILEDIR__}\${APPNAME}\LICENSE
LicenseForceSelection radiobuttons "I accept the agreement" "I do not accept the agreement"
SetCompressor /SOLID /FINAL lzma
RequestExecutionLevel admin
Unicode true


# Pages ------------------------------------
!define MUI_ABORTWARNING

!define MUI_ICON ${__FILEDIR__}\${APPNAME}\icon.ico

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY

!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\Apollo" 
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"

!insertmacro MUI_PAGE_STARTMENU ${APPNAME} $STARTMENUFOLDER

!insertmacro MUI_PAGE_LICENSE ${__FILEDIR__}\${APPNAME}\LICENSE 
!insertmacro MUI_PAGE_INSTFILES

!define MUI_FINISHPAGE_BUTTON "Finish" 
!define MUI_FINISHPAGE_CANCEL_ENABLED
!define MUI_FINISHPAGE_RUN $INSTDIR\${APPNAME}\${APPNAME}.exe
!define MUI_FINISHPAGE_RUN_TEXT "Run ${APPNAME} on exit"
!define MUI_FINISHPAGE_RUN_NOTCHECKED
!define MUI_FINISHPAGE_SHOWREADME ${__FILEDIR__}\${APPNAME}\readme.md 
!define MUI_FINISHPAGE_NOREBOOTSUPPORT
!insertmacro MUI_PAGE_FINISH


!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH


# Languages --------------------------------
!insertmacro MUI_LANGUAGE "English"

# Sections ---------------------------------
Section "Installing Apollo" install_sec
    SetOutPath "$INSTDIR"
    
    File /nonfatal /r ${__FILEDIR__}\${APPNAME}

    WriteRegStr HKCU "Software\Apollo" "Installdir" $INSTDIR
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    CreateShortcut $INSTDIR\${APPNAME}.lnk $INSTDIR\${APPNAME}\${APPNAME}.exe
    CreateShortcut $DESKTOP\${APPNAME}.lnk $INSTDIR\${APPNAME}\${APPNAME}.exe

    !insertmacro MUI_STARTMENU_WRITE_BEGIN ${APPNAME}

        ;Create shortcuts
        CreateDirectory "$SMPROGRAMS\$STARTMENUFOLDER"
        CreateShortcut $SMPROGRAMS\$STARTMENUFOLDER\${APPNAME}.lnk $INSTDIR\${APPNAME}\${APPNAME}.exe
        CreateShortcut "$SMPROGRAMS\$STARTMENUFOLDER\Uninstall.lnk" "$INSTDIR\Uninstall.exe"        

    !insertmacro MUI_STARTMENU_WRITE_END

SectionEnd

Section "Uninstall" uninstall_sec

    Delete "$INSTDIR\Uninstall.exe"
    Delete $INSTDIR\${APPNAME}.lnk 
    RMDir /r /REBOOTOK "$INSTDIR\${APPNAME}"    

    !insertmacro MUI_STARTMENU_GETFOLDER ${APPNAME} $StartMenuFolder

    Delete "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk"
    Delete $SMPROGRAMS\$STARTMENUFOLDER\${APPNAME}.lnk 
    RMDir "$SMPROGRAMS\$StartMenuFolder"

    DeleteRegKey /ifempty HKCU "Software\Apollo"

    RMDir /r /REBOOTOK "$INSTDIR"
SectionEnd
