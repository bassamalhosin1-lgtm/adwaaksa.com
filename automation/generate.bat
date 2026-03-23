@echo off
chcp 65001 >nul 2>&1
title CabltExperts Smart Generator
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║  🔧 أداة توليد المقالات الذكية           ║
echo  ║     CabltExperts Smart Generator          ║
echo  ╚══════════════════════════════════════════╝
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت! يرجى تثبيت Python 3.10+
    pause
    exit /b 1
)

:: Run the smart generator with all arguments passed to this bat
python "%~dp0smart_generator.py" %*

:: If no arguments given, show help
if "%~1"=="" (
    echo.
    echo  💡 أمثلة الاستخدام:
    echo.
    echo    generate.bat "كشف أعطال الكابلات تحت الأرض"
    echo    generate.bat "صيانة لوحات التوزيع" "فحص كابلات الجهد"
    echo    generate.bat --file keywords.txt
    echo    generate.bat --file keywords.txt --auto-push
    echo    generate.bat --list
    echo    generate.bat --check
    echo.
)

pause
