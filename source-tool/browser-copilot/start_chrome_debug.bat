@echo off
rem Script khoi chay Google Chrome hoac Microsoft Edge o che do Remote Debugging (port 9222)
rem Phuong an 2: Giup AI Agent ket noi truc tiep vao trinh duyet tren Windows

echo Dang tim trinh duyet Chrome / Edge...

set CHROME_EXE=""

if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set CHROME_EXE="C:\Program Files\Google\Chrome\Application\chrome.exe"
    goto launch
)
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set CHROME_EXE="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    goto launch
)
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set CHROME_EXE="%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
    goto launch
)
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    set CHROME_EXE="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    goto launch
)

echo Khong tim thay Chrome hoac Edge o thu muc mac dinh.
pause
exit /b 1

:launch
echo Tim thay trinh duyet: %CHROME_EXE%
echo Dang khoi chay tren cong Debug 9222...

start "" %CHROME_EXE% --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\CVAT_AI_Profile" "https://cvat.note.transformerlabs.ai"

echo Trinh duyet da mo. Ban chi can dang nhap CVAT va mo Job 1663.
echo Khi can bat dau Phuong an 2, chi can chay lenh: python copilot.py
