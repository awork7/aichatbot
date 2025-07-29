@echo off
echo 🏦 Setting up Production-Ready SIB Chatbot Structure...
echo ============================================================

REM Create main directory structure
mkdir api 2>nul
mkdir api\app 2>nul
mkdir api\app\routers 2>nul
mkdir api\app\models 2>nul
mkdir api\app\services 2>nul
mkdir api\app\core 2>nul
mkdir api\app\utils 2>nul
mkdir api\tests 2>nul
mkdir api\tests\unit 2>nul
mkdir api\tests\integration 2>nul

mkdir frontend 2>nul
mkdir frontend\src 2>nul
mkdir frontend\src\components 2>nul
mkdir frontend\src\services 2>nul
mkdir frontend\src\hooks 2>nul
mkdir frontend\src\utils 2>nul
mkdir frontend\public 2>nul

mkdir data-pipeline 2>nul
mkdir data-pipeline\processors 2>nul
mkdir data-pipeline\schedulers 2>nul

mkdir infrastructure 2>nul
mkdir infrastructure\docker 2>nul
mkdir infrastructure\kubernetes 2>nul

mkdir monitoring 2>nul
mkdir monitoring\prometheus 2>nul
mkdir monitoring\grafana 2>nul

mkdir data 2>nul
mkdir data\documents 2>nul
mkdir data\embeddings 2>nul
mkdir data\backups 2>nul

mkdir scripts 2>nul
mkdir docs 2>nul
mkdir docs\api 2>nul
mkdir logs 2>nul

REM Move existing files
echo Moving existing files to new structure...
if exist sib_data (
    xcopy sib_data data\documents\ /E /I /Q
    echo ✅ Moved sib_data to data\documents\
)

if exist sib_vectordb (
    xcopy sib_vectordb data\embeddings\ /E /I /Q
    echo ✅ Moved sib_vectordb to data\embeddings\
)

echo.
echo ✅ Production structure created successfully!
echo Next: Run the Python files provided to complete the setup.
pause
