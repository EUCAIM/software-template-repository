# Container provenance

The production image is:

```text
harbor.eucaim.cancerimage.eu/processing-tools/nnunet-colon-cancer:1.0.0
```

The task definition in `task_containers/colon/dockerfile` is built from
the shared `nnunet:base` image. That base provides CUDA, nnU-Net v1, MITK, and
the DICOM conversion scripts; the task image adds the
`Task010_Colon` pretrained model at build time.

The final image command is `/bin/bash /app/start_nnunet.sh`. It converts input
DICOM series to NIfTI, executes `nnUNet_predict` in `3d_fullres` mode, and
converts predictions to DICOM SEG.

`nnunet:base` is a build-only dependency, not an EUCAIM tool or FEM runtime
dependency. It is built from the
[nnunet-eucaim-docker repository](https://github.com/MIC-DKFZ/nnunet-eucaim-docker)
at commit `c1bbba939516d0a6c45b89074f018fc5ab566f7d`. The base build context
includes `nnunet-base/Dockerfile`, `nnunet-base/start_nnunet.sh`, and
`nnunet-base/nnunetv1.patch`. The container sources are Apache-2.0 licensed.
