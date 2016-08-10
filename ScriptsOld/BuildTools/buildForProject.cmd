echo %date% %time%

c:
set ProjectFolder=%1
set ProjectFile=%2
set doClean=%3

cd %ProjectFolder%


REM ******************%ProjectFile%***********************************************************************************************************
IF "%doClean%"=="noClean" GOTO START_BUILD
msbuild /t:Clean  /v:quiet "%ProjectFile%" 

:START_BUILD
msbuild /clp:ErrorsOnly /t:Make /v:quiet "%ProjectFile%"

REM ******************end %ProjectFile%*******************************************************************************************************


REM remove big and not needed files
for  /r %ProjectFolder%  %%B in (*.cbproj) do (
   del /s/q *.log *.pch *.obj *.tds *.ils *.ilf *.ilc *.ild *.res *.map >nul
   )
   
