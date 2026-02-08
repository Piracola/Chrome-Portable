@echo off
chcp 65001 >nul

set "APP_DIR=%~dp0Chrome"
set "CHROME_EXE="

:: 只遍历 Chrome 文件夹
for /d %%d in ("%APP_DIR%*") do (
    if exist "%%d\chrome.exe" (
        set "CHROME_EXE=%%d\chrome.exe"
        goto :found
    )
)

echo 未找到版本目录中的 chrome.exe
pause
exit /b 1

:found
powershell -NoProfile -ExecutionPolicy Bypass -Command "$s=New-Object -ComObject WScript.Shell; $l=$s.CreateShortcut('%~dp0chrome.lnk'); $l.TargetPath='%CHROME_EXE%'; $l.Arguments='--disable-background-networking'; $l.WorkingDirectory='%~dp0'; $l.IconLocation='%CHROME_EXE%,0'; $l.Save()"

if exist "%~dp0chrome.lnk" (
    echo 快捷方式创建成功
    echo 指向：%CHROME_EXE%
    exit /b 0
) else (
    echo 快捷方式创建失败
    pause
    exit /b 1
)
