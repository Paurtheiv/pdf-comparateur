@echo off
setlocal enabledelayedexpansion

REM 1. Définir chemins
set ROOT=%~dp0
set PYDIR=%ROOT%python
set ZIP=%ROOT%python_embed.zip
set VENV=%ROOT%venv

REM 2. Installer Python si besoin
if not exist "%PYDIR%\python.exe" (
    echo Extraction de Python embarqué...
    powershell -Command "Expand-Archive -Path '%ZIP%' -DestinationPath '%PYDIR%'"
) else (
    echo Python embarqué déjà présent.
)

REM 3. Mettre python.exe dans le PATH
set PATH=%PYDIR%;%PATH%

REM 4. Créer venv si besoin
if not exist "%VENV%\Scripts\activate.bat" (
    echo Creation de l'environnement virtuel...
    python -m venv "%VENV%"
) else (
    echo Environnement virtuel deja cree.
)

REM 5. Activer venv
call "%VENV%\Scripts\activate.bat"

REM 6. Installer dependances
echo Installation des dependances...
pip install --upgrade pip
pip install -r requirements.txt

REM 7. Lancer l'application Streamlit
echo Lancement de l'application...
streamlit run app_streamlit.py

pause
