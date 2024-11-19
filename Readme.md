# Brain Extraction Pipeline with HDBET (Docker and Signgularity)

This project provides a simple docker/singularity pipeline for **defacing** from NIfTI MRI (`.nii.gz`) files using skull-stripping **HD-BET** and then dilation. 

## Prerequisites

Before setting up and running the pipeline, ensure that your system meets the following requirements:

### 0. Download the HDBET Repository
Link: https://github.com/MIC-DKFZ/HD-BET

### 1. Docker Or Singularity

- **Installation**: Docker must be installed and running on your system. Follow the [official Docker installation guide](https://docs.docker.com/get-docker/) for your operating system. Follow the [official Singularity installation guide](https://sylabs.io/guides/3.7/user-guide/installation.html) for your operating system.

**(Optional for GPU Support)**

If you intend to leverage GPU acceleration for faster processing, ensure the following:

- **NVIDIA GPU**: Your system should have an NVIDIA GPU.
- **NVIDIA Drivers**: Install the latest NVIDIA drivers compatible with your GPU.
- **NVIDIA Docker (`nvidia-container-toolkit`)**: Enables Docker containers to access NVIDIA GPUs.
-  Install NVIDIA Docker

## Project Structure

The project directory as follows:

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

- **input_nifti/**: Directory containing input NIfTI files.
- **output/**: Directory where the processed brain-extracted NIfTI files will be saved.

## Building the Docker Image

Navigate to your project directory and build the Docker image using the provided `Dockerfile`.

```bash
cd path/to/brain_extraction_project
docker build -t brain-extraction:latest .
```

Once the image is built, you can run the container to execute your Python script. Depending on whether you have GPU support, follow the appropriate instructions below.

### With GPU Support (NVIDIA Docker)

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

### Without GPU Support (Docker)

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

### Running the Container with GPU (Docker)

```bash
docker run --gpus all \
    -v /home/user/brain_extraction_project/input_nifti:/input \
    -v /home/user/brain_extraction_project/output:/output \
    brain-extraction:latest \
    --input_dir /input \
    --output_path /output \
    --CUDA_VISIBLE_DEVICES 0
```
## Singularity (using defacer.def)
Note: this is not tested, if you do, please let me know if it works or not :) 

To build the Singularity image and run the container, execute the following commands:
```
sudo singularity build defacer.sif Singularity.def
singularity run defacer.sif
```
OR if you want to pass the input and output directories as arguments:
```
singularity run defacer.sif --input /path/to/input --output /path/to/output
```

## License

This project is licensed under the [MIT License](LICENSE).

---

**Note**: Replace placeholder paths (e.g., `/home/user/brain_extraction_project/`) with actual paths relevant to your environment. Ensure that all dependencies and scripts are correctly referenced and that directory permissions are appropriately set to allow Docker to access necessary files.

For any further assistance or questions, feel free to open an issue or contact the maintainer.

