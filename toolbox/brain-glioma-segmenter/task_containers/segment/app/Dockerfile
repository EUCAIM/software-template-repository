FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime
RUN apt-get -y update
RUN apt-get -y install gcc

USER root
COPY ./mlcube_project24/requirements.txt /project/requirements.txt 
RUN pip3 install  --no-cache-dir  -r /project/requirements.txt


COPY ./mlcube_project24/nnUNet /project/nnUNet 
COPY ./mlcube_project24/mednext /project/mednext 

RUN pip3 install -e /project/nnUNet/.
RUN pip3 install -e /project/mednext/.


ENV LANG=C.UTF-8

COPY ./mlcube_project24/checkpoints /mlcube_inferer/checkpoints
COPY ./mlcube_project23/checkpoints /mlcube_inferer/checkpoints
COPY ./mlcube_project24/infer_low_disk_glioma_mednext.py /mlcube_project/infer_low_disk_glioma_mednext.py
COPY ./mlcube_project23/infer_low_disk.py /mlcube_project/infer_low_disk.py

COPY ./mlcube_project23/surface_distance /mlcube_project/surface_distance
COPY ./mlcube_project23/postproc /mlcube_project/postproc
COPY ./mlcube_project23/pp_radiomics /mlcube_project/pp_radiomics
COPY ./mlcube_project23/pp_cluster /mlcube_project/pp_cluster
COPY ./mlcube_project23/fops /mlcube_project/fops
COPY /mlcube_project23/kmeans-cluster-artifacts /mlcube_project/kmeans-cluster-artifacts

RUN chmod -R 777 /project
COPY ./mlcube_project24/mlcube_infer24.py /mlcube_project/mlcube_infer24.py
COPY ./mlcube_project23/mlcube_infer23.py /mlcube_project/mlcube_infer23.py
COPY ./mlcube_project23/default_mask /mlcube_project/default_mask
COPY ./runner.py /mlcube_project/runner.py

WORKDIR /mlcube_project

RUN chmod -R 777 /mlcube_project
CMD ["python", "runner.py", "-i", "/input", "-o", "/output", "-t", "GLI"]