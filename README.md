# Baby Faces Anonymizer

An end-to-end pipeline for ingesting, annotating, training, and deploying a model to anonymize baby faces in images.

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Setup](#2-setup)
3. [Pipeline Execution](#3-pipeline-execution)
   - [Using Scripts](#31-using-scripts-recommended)
   - [Manual Execution](#32-manual-execution)
4. [Serving the Model](#4-serving-the-model)
   - [Docker Method](#41-docker-method)
   - [Manual Serving](#42-manual-serving)

## 1. Prerequisites

- NVIDIA GPU with CUDA support (required for training, recommended for serving)
- Docker (for containerized execution)
- Python 3.10+

## 2. Setup

### Google Search Engine Configuration
1. Rename `.env.example` to `.env`
2. Create a new search engine at [Search Engine Control Panel](https://programmablesearchengine.google.com/controlpanel/all)
3. Copy the Search Engine ID to `SEARCH_ENGINE_ID` in `.env`
4. Generate a Google Cloud API key and add it to `G_API_KEY` in `.env`

### Environment Setup
We recommend using either:
- The provided devcontainer configuration
- NVIDIA's PyTorch container: `nvcr.io/nvidia/pytorch:23.07-py3`

To use the NVIDIA container:
```bash
docker run --gpus all -it --rm -v $(pwd):/workspace nvcr.io/nvidia/pytorch:23.07-py3
```

## 3. Pipeline Execution

### 3.1 Using Scripts (Recommended)

#### Installation:
```bash
./setup_train.sh  # Installs all training dependencies
```

#### Run Full Pipeline:
```bash
./run_pipe.sh  # Executes mining, annotation, and training
```

### 3.2 Manual Execution

#### 1. Image Mining
```bash
python src/scripts/mine.py data/queries.txt data/mined
```

#### 2. Image Annotation
```bash
python src/scripts/annotate.py data/mined data/annots
```

#### 3. Dataset Preparation
```bash
python src/scripts/split.py data/mined data/annots output/data
```

#### 4. Model Training
```bash
python src/scripts/train.py
```

## 4. Serving the Model

### 4.1 Docker Method

#### Build the image:
```bash
docker build -t baby-face-anonymizer .
```

#### Run the container:
```bash
docker run --gpus all -p 8000:8000 baby-face-anonymizer:latest
```
Access the API at: `http://localhost:8000/`

### 4.2 Manual Serving

#### Install dependencies:
```bash
./setup_infer.sh  # or manually:
pip install -r requirements.txt
sudo apt update && sudo apt install -y ffmpeg
```

#### Run the API:
```bash
fastapi run api.py
```

## Additional Notes

- For GPU acceleration, ensure you have NVIDIA drivers installed and Docker configured with GPU support
- The training process requires GroundingDINO - the setup script handles this installation
- Model weights will be saved in the `weights/` directory after training