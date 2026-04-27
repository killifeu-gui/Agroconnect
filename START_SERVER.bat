@echo off
REM Démarrage simple d'AgroConnect
cd /d "%~dp0"

echo.
echo ============================================================
echo   AGROCONNECT - Démarrage du serveur
echo ============================================================
echo.

REM Activer venv
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

REM Définir variables
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=False

echo.
echo   Serveur démarre sur: http://127.0.0.1:5000
echo.
echo   Identifiants test:
echo   - Username: babacar_agro
echo   - Password: agroconnect2024
echo.
echo ============================================================
echo.

REM Lancer l'app
python app.py

pause
