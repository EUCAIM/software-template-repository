FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y python3-pip python3-dev

RUN pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118

COPY ./requirements.txt /mlcube_project/requirements.txt 

RUN pip install --no-cache-dir -r /mlcube_project/requirements.txt


COPY ./nnUNet /mlcube_project/nnUNet 
RUN pip install -e /mlcube_project/nnUNet/.

ENV LANG C.UTF-8

COPY . /mlcube_project

ENTRYPOINT ["python3", "/mlcube_project/mlcube.py"]