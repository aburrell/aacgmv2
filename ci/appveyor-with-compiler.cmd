:: To build extensions for 64 bit Python 3, we need to configure environment
:: variables to use the MSVC 2010 C++ compilers from GRMSDKX_EN_DVD.iso of:
:: MS Windows SDK for Windows 7 and .NET Framework 4 (SDK v7.1)
::
:: To build extensions for 64 bit Python 2, we need to configure environment
:: variables to use the MSVC 2008 C++ compilers from GRMSDKX_EN_DVD.iso of:
:: MS Windows SDK for Windows 7 and .NET Framework 3.5 (SDK v7.0)
::
:: 32 bit builds do not require specific environment configurations.
::
:: Note: this script needs to be run with the /E:ON and /V:ON flags for the
:: cmd interpreter, at least for (SDK v7.0)
::
:: More details at:
:: https://github.com/cython/cython/wiki/64BitCythonExtensionsOnWindows
:: http://stackoverflow.com/a/13751649/163740
::
:: Author: Olivier Grisel
:: License: CC0 1.0 Universal: http://creativecommons.org/publicdomain/zero/1.0/
::
:: Adapted for Visual Studio 2017 (AGB)
:: See: https://www.appveyor.com/docs/lang/cpp/#visual-studio-2017
SET COMMAND_TO_RUN=%*
SET WIN_WDK="c:\Program Files (x86)\Windows Kits\10\Include\wdf"
ECHO ARCH: %PYTHON_ARCH%


IF "%PYTHON_VERSION%"=="3.6" (
    IF EXIST %WIN_WDK% (
        REM See: https://connect.microsoft.com/VisualStudio/feedback/details/1610302/
        REN %WIN_WDK% 0wdf
    )
    GOTO main
)

CALL "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars%PYTHON_ARCH%.bat"

:main

ECHO Executing: %COMMAND_TO_RUN%
CALL %COMMAND_TO_RUN% || EXIT 1
