#!/bin/bash
# Helper script for Docker Getting Started lab

echo "🐳 Docker Getting Started Lab Demo (Python)"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in your PATH."
    echo "Please install Docker according to the instructions in the lab README."
    exit 1
fi

echo "✅ Docker is installed."
echo ""

echo "⚠️  Before running this script, make sure you've completed the TODOs in:"
echo "   - Dockerfile"
echo "   - app.py"
echo ""
echo "👉 If you haven't completed these TODOs, the build or run will fail."
echo ""

echo "👉 Building the Python demo image..."
echo "   This will use your Dockerfile implementation."
docker build -t docker-getting-started-py .

if [ $? -ne 0 ]; then
    echo "❌ Build failed. Please check your Dockerfile implementation."
    exit 1
fi

echo ""
echo "👉 Running the container on port 8080..."
echo "Visit http://localhost:8080 in your browser to see the demo."
echo ""
echo "Use Ctrl+C to stop the container when you're done."
echo ""

# TODO: Modify this run command to experiment with:
# - Setting environment variables (-e KEY=VALUE)
# - Volume mounts (-v host_path:container_path)
# - Different port mappings
docker run --rm -it -p 8080:80 --name docker-lab-py docker-getting-started-py 