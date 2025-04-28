# Docker Layer Analysis Tools

This directory contains tools and examples to help you analyze Docker image layers. Understanding how layers work is essential for creating optimized Docker images.

## Available Tools

1. **layer-analysis-windows.bat** - A Windows batch script to analyze Docker image layers
2. **dive-commands.sh** - A Linux/Mac shell script to run the Dive tool for detailed layer analysis
3. **layer-analysis-linux.sh** - A Linux shell script similar to the Windows version
4. **Dockerfile** - An intentionally inefficient Dockerfile for you to analyze and improve

## Analysis Tasks

### Task 1: Analyze the Provided Dockerfile

The `Dockerfile` in this directory contains numerous inefficient practices commonly seen in real-world Dockerfiles. Your task is to:

1. Analyze the problems in the Dockerfile (follow the TODOs in the file)
2. Create a new file called `layer_analysis.md` to document your findings
3. In your `layer_analysis.md` file, explain how each issue impacts the final image size and build performance
4. Propose optimizations for each issue

**Note:** You must create the `layer_analysis.md` file yourself and document your own analysis. Do not copy from external sources. The goal is to develop your understanding of Docker layer optimization.

### Task 2: Build and Analyze Images

Build a Docker image using the provided Dockerfile:

```bash
docker build -t analysis-demo:unoptimized .
```

Then use the analysis tools to inspect its layers:

#### For Windows Users:
```bash
layer-analysis-windows.bat analysis-demo:unoptimized
```

#### For Linux/Mac Users:
```bash
chmod +x dive-commands.sh
./dive-commands.sh analysis-demo:unoptimized
```

or:
```bash
chmod +x layer-analysis-linux.sh
./layer-analysis-linux.sh analysis-demo:unoptimized
```

### Task 3: Implement Optimizations

After analyzing the issues:

1. Create a new Dockerfile called `Dockerfile.optimized` with your improvements
2. Build a new image using your optimized Dockerfile:
   ```bash
   docker build -t analysis-demo:optimized -f Dockerfile.optimized .
   ```
3. Compare the size and layer count of both images:
   ```bash
   docker images | grep analysis-demo
   ```

**Note:** Your `Dockerfile.optimized` should be your own implementation based on your analysis. Do not just copy a solution from elsewhere. The exercise is designed to help you practice optimizing Docker images.

## Using Dive Tool

The Dive tool provides an interactive UI to explore Docker image layers:

```bash
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  wagoodman/dive:latest <your-image>
```

### Key Features of Dive:

- Interactive layer exploration
- Efficiency analysis
- Wasted space identification
- Layer-by-layer comparison

## Understanding Docker History

The `docker history` command provides a quick view of image layers:

```bash
docker history <your-image>
```

This shows:
- Layer sizes
- Creation times
- Commands that created each layer

## Expected Deliverables

1. A completed `layer_analysis.md` file documenting the inefficiencies in the original Dockerfile
2. A new `Dockerfile.optimized` implementing your improvements
3. A comparison of image sizes and layer counts between the original and optimized versions

## Clean Up

```bash
docker rmi analysis-demo:unoptimized analysis-demo:optimized
``` 