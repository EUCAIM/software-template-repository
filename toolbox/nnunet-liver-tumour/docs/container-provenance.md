# Container provenance

The production image is:

```text
harbor.eucaim.cancerimage.eu/processing-tools/nnunet-liver-tumour:1.0.0
```

The task definition in `task_containers/liver/dockerfile` is built from
the shared `nnunet:base-1.0.0` image. That base provides CUDA, nnU-Net v1,
MITK, and the DICOM conversion scripts; the task image adds the
`Task029_LiTS` pretrained model at build time.

The final image command is `/bin/bash /app/start_nnunet.sh`. It converts input
DICOM series to NIfTI, executes `nnUNet_predict` in `3d_fullres` mode, and
converts predictions to DICOM SEG.

`nnunet:base-1.0.0` is a build-only dependency, not an EUCAIM tool or FEM
runtime dependency. It is built from the
[nnunet-eucaim-docker repository](https://github.com/MIC-DKFZ/nnunet-eucaim-docker)
at commit `084b4f1371869b3cc8eeda7d60e14d3d613b5f2a`. The base build context
includes `nnunet-base/Dockerfile`, `nnunet-base/start_nnunet.sh`,
`nnunet-base/entrypoint.sh`, `nnunet-base/scripts/`, and
`nnunet-base/nnunetv1.patch`. The container sources are Apache-2.0 licensed.
