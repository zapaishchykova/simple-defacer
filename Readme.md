```markdown
# Brain Extraction Pipeline with Docker

This project provides a streamlined pipeline for **brain extraction** from NIfTI (`.nii.gz`) files using **HDBET** within a Dockerized environment. Leveraging Docker ensures a consistent and reproducible setup, simplifying the deployment and execution process across different systems.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Building the Docker Image](#building-the-docker-image)
- [Running the Docker Container](#running-the-docker-container)
  - [With GPU Support](#with-gpu-support)
  - [Without GPU Support](#without-gpu-support)
- [Example Usage](#example-usage)
- [License](#license)

## Overview

This pipeline automates the process of skull stripping and brain extraction from neuroimaging data. It utilizes **HDBET** for accurate brain extraction and processes multiple NIfTI files in batches. The entire setup is encapsulated within a Docker container to ensure environment consistency and ease of deployment.

## Prerequisites

Before setting up and running the pipeline, ensure that your system meets the following requirements:

### 0. Download the HDBET Repository
Link: https://github.com/MIC-DKFZ/HD-BET

### 1. Docker

- **Installation**: Docker must be installed and running on your system. Follow the [official Docker installation guide](https://docs.docker.com/get-docker/) for your operating system.

### 2. NVIDIA Docker (Optional for GPU Support)

If you intend to leverage GPU acceleration for faster processing, ensure the following:

- **NVIDIA GPU**: Your system should have an NVIDIA GPU.
- **NVIDIA Drivers**: Install the latest NVIDIA drivers compatible with your GPU.
- **NVIDIA Docker (`nvidia-container-toolkit`)**: Enables Docker containers to access NVIDIA GPUs.
-  Install NVIDIA Docker

## Project Structure

Organize your project directory as follows:

```
brain_extraction_project/
│
├── Dockerfile
├── defacer.py
├── HDBET/
│   ├── HD_BET/
│   │   ├── run.py
│   │   └── config.py
│   └── ... (other HDBET files)
├── input_nifti/
│   ├── subject1.nii.gz
│   ├── subject2.nii.gz
│   └── ...
└── output/  # Optional; the script can create it
```

- **Dockerfile**: Defines the Docker image configuration.
- **defacer.py**: Your main Python script for brain extraction.
- **HDBET/**: Directory containing the HDBET tool and its dependencies.
- **input_nifti/**: Directory containing input NIfTI files.
- **output/**: Directory where the processed brain-extracted NIfTI files will be saved.

## Building the Docker Image

Navigate to your project directory and build the Docker image using the provided `Dockerfile`.

```bash
cd path/to/brain_extraction_project
docker build -t brain-extraction:latest .
```

**Explanation**:

- `docker build`: Command to build a Docker image.
- `-t brain-extraction:latest`: Tags the image with the name `brain-extraction` and the tag `latest`.
- `.`: Specifies the current directory as the build context.

**Expected Output**:

The build process will execute each step in the `Dockerfile`. It may take several minutes, especially when installing dependencies. Upon successful completion, you'll see a message indicating that the image has been built.

```
Step 1/...
...
Successfully built abcdef123456
Successfully tagged brain-extraction:latest
```

## Running the Docker Container

Once the image is built, you can run the container to execute your Python script. Depending on whether you have GPU support, follow the appropriate instructions below.

### With GPU Support

If you have an NVIDIA GPU and NVIDIA Docker installed, run the container with GPU access:

```bash
docker run --gpus all \
    -v /absolute/path/to/input_nifti:/input \
    -v /absolute/path/to/output:/output \
    brain-extraction:latest \
    --input_dir /input \
    --output_path /output \
    --CUDA_VISIBLE_DEVICES 0
```

**Parameters**:

- `--gpus all`: Grants the container access to all available GPUs.
- `-v /absolute/path/to/input_nifti:/input`: Mounts the local `input_nifti` directory to `/input` inside the container.
- `-v /absolute/path/to/output:/output`: Mounts the local `output` directory to `/output` inside the container.
- `brain-extraction:latest`: Specifies the Docker image to use.
- `--input_dir /input`: Argument passed to `defacer.py` specifying the input directory inside the container.
- `--output_path /output`: Argument specifying the output directory inside the container.
- `--CUDA_VISIBLE_DEVICES 0`: Sets the CUDA device ID to use.

### Without GPU Support

If you don't have a GPU or prefer to run the container without GPU acceleration:

```bash
docker run \
    -v /absolute/path/to/input_nifti:/input \
    -v /absolute/path/to/output:/output \
    brain-extraction:latest \
    --input_dir /input \
    --output_path /output \
    --CUDA_VISIBLE_DEVICES -1
```

**Note**: Setting `--CUDA_VISIBLE_DEVICES` to `-1` typically indicates that no GPU should be used.

## Example Usage

Assuming the following:

- **Project Directory**: `/home/user/brain_extraction_project/`
- **Input Directory**: `/home/user/brain_extraction_project/input_nifti/`
- **Output Directory**: `/home/user/brain_extraction_project/output/`

### Building the Image

```bash
cd /home/user/brain_extraction_project/
docker build -t brain-extraction:latest .
```

### Running the Container with GPU

```bash
docker run --gpus all \
    -v /home/user/brain_extraction_project/input_nifti:/input \
    -v /home/user/brain_extraction_project/output:/output \
    brain-extraction:latest \
    --input_dir /input \
    --output_path /output \
    --CUDA_VISIBLE_DEVICES 0
```

### Running the Container Without GPU

```bash
docker run \
    -v /home/user/brain_extraction_project/input_nifti:/input \
    -v /home/user/brain_extraction_project/output:/output \
    brain-extraction:latest \
    --input_dir /input \
    --output_path /output \
    --CUDA_VISIBLE_DEVICES -1
```


### Interactive Debugging

For interactive debugging, run the container with an interactive shell:

```bash
docker run --gpus all -it \
    -v /home/user/brain_extraction_project/input_nifti:/input \
    -v /home/user/brain_extraction_project/output:/output \
    brain-extraction:latest \
    /bin/bash
```

Once inside the container, manually execute your Python script or inspect the filesystem:

```bash
python /defacer.py --input_dir /input --output_path /output --CUDA_VISIBLE_DEVICES 0
```

docker run --gpus all \
    -v /media/sdb/Anna/defacer/input_nifti:/input \
    -v /media/sdb/Anna/defacer/output:/output \
    brain-extraction \
    --input_dir /input \
    --output_path /output \
    --CUDA_VISIBLE_DEVICES 0


## License

This project is licensed under the [MIT License](LICENSE).

---

**Note**: Replace placeholder paths (e.g., `/home/user/brain_extraction_project/`) with actual paths relevant to your environment. Ensure that all dependencies and scripts are correctly referenced and that directory permissions are appropriately set to allow Docker to access necessary files.

For any further assistance or questions, feel free to open an issue or contact the maintainer.

