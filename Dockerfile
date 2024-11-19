FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-runtime

USER 0
#this is for time zone setting
ENV TZ=US/Eastern
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y tzdata

# this is for opencv
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# install python3.8
RUN apt update && \
    apt install --no-install-recommends -y build-essential software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install --no-install-recommends -y python3.8 python3-pip python3-setuptools python3-distutils && \
    apt-get install -y wget && \
    apt clean && rm -rf /var/lib/apt/lists/*
RUN python3.8 -m pip install --upgrade pip 

#RUN conda update -n base -c defaults conda
RUN python3 -m pip install --upgrade pip
RUN pip install statsmodels==0.12.1 torchaudio==0.10.0 torchvision==0.11.1
RUN pip install SimpleITK itk-elastix imageio matplotlib opencv-python pandas \
    scikit-image scikit-learn scipy nibabel 
    
# Alternatively, if HDBET is a Python package, install it directly
# Assuming HDBET has a setup.py in the cloned repository
COPY HDBET/ /HDBET/

# Copy your Python script into the container
# Replace 'defacer.py' with the actual name of your script if different
COPY defacer.py /defacer.py

# (Optional) If you have other scripts or resources, copy them as needed
# COPY other_script.py /other_script.py

# Create necessary directories (temp and output) if they are expected to be present
# Alternatively, your script can handle directory creation
RUN mkdir -p /temp /output

# Set environment variables for MKL (as per your original Dockerfile)
ENV MKL_SERVICE_FORCE_INTEL=1

# Set the working directory
WORKDIR /

# Ensure the script has execution permissions
RUN chmod +x /defacer.py

# Set the entrypoint to execute your script
ENTRYPOINT ["python", "/defacer.py"]
