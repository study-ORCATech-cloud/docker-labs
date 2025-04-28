@echo off
:: Script to analyze Docker images in Windows

:: Check if image name is provided
if "%~1"=="" (
    echo Usage: %0 [image_name]
    echo Example: %0 layers-demo:unoptimized
    exit /b 1
)

set IMAGE_NAME=%~1

echo Analyzing Docker image: %IMAGE_NAME%
echo ==========================================
echo.

:: Standard Docker commands for layer analysis
echo Running docker history:
docker history %IMAGE_NAME%

echo.
echo Running docker image inspect:
docker image inspect %IMAGE_NAME% | findstr /C:"Size" /C:"Id" /C:"Created"

echo.
echo To analyze with dive tool, run:
echo docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest %IMAGE_NAME% 