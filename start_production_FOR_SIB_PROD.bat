@echo off
echo 🏦 Starting SIB Chatbot Production Environment
echo ============================================

echo Stopping existing containers...
docker-compose down

echo Building and starting services...
docker-compose up --build -d

echo Waiting for services to start...
timeout /t 10 /nobreak > nul

echo Checking service health...
curl -f http://localhost:8000/health || echo "API not ready yet"

echo.
echo ✅ Production environment started!
echo.
echo Available services:
echo - API: http://localhost:8000
echo - API Docs: http://localhost:8000/docs
echo - Prometheus: http://localhost:9090
echo - Grafana: http://localhost:3001 (admin/admin)
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down
pause
