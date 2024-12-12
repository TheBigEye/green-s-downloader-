@ECHO OFF


:: Requirements to run this script:
:: - Have Windows 7 (With UCRT update) or Windows 10
:: - Have 'pyinstaller' and 'pyinstaller-versionfile' modules installed with pip
:: - Have a brain


:: Obtains the current .bat file dir
SET PROJECT_PATH=%~dp0
SET PROJECT_PATH=%PROJECT_PATH:~0,-1%


:: Creates the Build folder
IF NOT EXIST "%PROJECT_PATH%\build" (
    MKDIR "%PROJECT_PATH%\build"
)


:: Call the functions in order
GOTO :MAIN


:: Define a function to clean old build resources
:PRE_CLEAN

ECHO [i] Pre-cleaning old build resources ...
RD /Q /S "build" > NUL 2>&1
DEL /Q /F "metadata.rc" > NUL 2>&1
DEL /Q /F "main.spec" > NUL 2>&1
DEL /Q /F "main.exe" > NUL 2>&1
PING -N 3 127.0.0.1 > NUL

EXIT /B 0


:: Define a function to compile Python code into an EXE file
:COMPILE_PYTHON

ECHO [i] Compiling from python to a native executable ...

:: Create the fixed version file for the .exe
create-version-file "metadata.yml" --outfile "metadata.rc"

pyinstaller --clean --onefile --windowed --noupx --distpath "./" --specpath "./" --workpath "build" --version-file "metadata.rc" --icon "resources/icon.ico" --add-data "resources/icon.png;resources" "main.py"

PING -N 3 127.0.0.1 > NUL

EXIT /B 0


:: Define a function to clean up the build resources
:POST_CLEAN

ECHO [i] Post-cleaning build resources ...
RD /Q /S "build" > NUL 2>&1
DEL /Q /F "metadata.rc" > NUL 2>&1
DEL /Q /F "main.spec" > NUL 2>&1
PING -N 3 127.0.0.1 > NUL

EXIT /B 0


:: Main routine
:MAIN

CALL :PRE_CLEAN
PAUSE
CLS

CALL :COMPILE_PYTHON
PAUSE
CLS

CALL :POST_CLEAN
PAUSE
CLS

EXIT /B 0
