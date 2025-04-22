@echo off
:: Helper script for Docker Getting Started lab on Windows

echo 🐳 Docker Getting Started Lab Demo (Python)
echo ==========================================
echo.

:: Check if Docker is installed
docker --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed or not in your PATH.
    echo Please install Docker according to the instructions in the lab README.
    exit /b 1
)

echo ✅ Docker is installed.
echo.

echo 👉 Building the Python demo image...
docker build -t docker-getting-started-py .

echo.
echo 👉 Running the container on port 8080...
echo Visit http://localhost:8080 in your browser to see the demo.
echo.
echo Use Ctrl+C to stop the container when you're done.
echo.

:: Run in interactive mode so Ctrl+C works to stop
docker run --rm -it -p 8080:80 --name docker-lab-py docker-getting-started-py 