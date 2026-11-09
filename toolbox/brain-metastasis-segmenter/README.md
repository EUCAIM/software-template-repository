# Brain Metastasis Segmenter (BraTS-MET)

Official EUCAIM integration repository for **Brain Metastasis Segmenter (BraTS-MET)**, developed by Biomedical Image Technologies, Universidad Politécnica de Madrid (BIT-UPM) and Pediatric Accelerated Intelligence Lab, Sheikh Zayed Institute for Pediatric Surgical Innovation, Children's National Hospital.

## Overview & Intended Use
Performs automated multi-compartment segmentation of brain metastases and resection cavities (BraTS-MET) on structural MRI using deep ensembled convolutional networks and radiomics clustering.

The tool is pre-packaged as a containerized solution registered in the EUCAIM Harbor registry.

## Harbor Registry Information
- **Image URI:** `harbor.eucaim.cancerimage.eu/processing-tools/brain-metastasis-segmenter:v1.0.0`
- **Architecture:** `x86_64` (`linux/amd64`)
- **Version:** `1.0.0`
- **Default User:** `appuser` (non-root UID `1000`)

## Hardware Requirements
- **CPU:** x86_64 architecture, 4+ physical cores recommended.
- **RAM:** Minimum 16 GB system memory (shared memory `--shm-size=4G` recommended).
- **GPU:** NVIDIA CUDA-compatible GPU (minimum 8 GB VRAM, 16 GB+ VRAM recommended for high throughput).
- **Disk:** 15 GB available disk space for temporary inference arrays.

## Network Requirements
- **Offline:** `0` incoming/outgoing network connections required at runtime (`--network none`). All model checkpoints and dependencies are bundled or managed locally.

## Input & Output Specifications

### Input Directory Format (EUCAIM Common Data Model / BraTS)
The tool expects a directory containing one or more patient/study subdirectories. Each study directory must contain the 4 co-registered, skull-stripped NIfTI volumes:

```text
input/
└── <STUDY_ID>/
    ├── <STUDY_ID>-t1n.nii.gz    # T1-weighted native
    ├── <STUDY_ID>-t1c.nii.gz    # T1-weighted post-contrast
    ├── <STUDY_ID>-t2w.nii.gz    # T2-weighted
    └── <STUDY_ID>-t2f.nii.gz    # T2-weighted FLAIR
```

### Output Directory Format
For each study processed, the container outputs a predicted 3D segmentation mask directly into the output directory:

```text
output/
└── <STUDY_ID>.nii.gz
```

## Standalone Docker Usage

```bash
docker run --rm \
  --network none \
  --gpus all \
  --memory=16G --shm-size=4G \
  -v /path/to/input:/input:ro \
  -v /path/to/output:/output:rw \
  harbor.eucaim.cancerimage.eu/processing-tools/brain-metastasis-segmenter:v1.0.0
```

Where:
- `/path/to/input` is mounted read-only (`:ro`) containing patient folders.
- `/path/to/output` is mounted read-write (`:rw`) to store generated `.nii.gz` masks.

## Data Provenance & Terms of Use
The sample MRI volume provided in `test/example_input/` is strictly intended for technical integration testing, unit verification, and CI/CD validation within the EUCAIM platform. The imaging data originates from the Brain Tumor Segmentation (BraTS) Challenge benchmarks organized under the auspices of MICCAI and Sage Bionetworks (Synapse).

Use, distribution, or reproduction of BraTS data beyond technical integration testing requires registration and adherence to the official BraTS Data Use Agreement at [synapse.org](https://www.synapse.org/brats). This data is strictly for Research Use Only (RUO).

## Citations
If you use or refer to this software in your research or EUCAIM studies, please cite:

- Capellán-Martín, D., Parida, A., Jiang, Z., Kulkarni, N., Iyer, K., Tapp, A., ... & Linguraru, M. G. (2025, September). Adaptable Segmentation Pipeline for Diverse Brain Tumors with Radiomic-Guided Subtyping and Lesion-Wise Model Ensemble. In *International Conference on Medical Image Computing and Computer-Assisted Intervention* (pp. 456-467). Cham: Springer Nature Switzerland.
- Capellán-Martín, D., Jiang, Z., Parida, A., Liu, X., Lam, V., Nisar, H., ... & Linguraru, M. G. (2023). Model ensemble for brain tumor segmentation in magnetic resonance imaging. In *International Challenge on Cross-Modality Domain Adaptation for Medical Image Segmentation* (pp. 221-232). Springer Nature Switzerland. https://doi.org/10.1007/978-3-031-76163-8_20
- Jiang, Z., Capellán-Martín, D., Parida, A., Tapp, A., Liu, X., Ledesma-Carbayo, M. J., ... & Linguraru, M. G. (2024). Magnetic Resonance Imaging Feature-Based Subtyping and Model Ensemble for Enhanced Brain Tumor Segmentation. *arXiv preprint arXiv:2412.04094*. https://doi.org/10.48550/arXiv.2412.04094
- Jiang, Z., Capellán-Martín, D., Parida, A., Liu, X., Ledesma-Carbayo, M. J., Anwar, S. M., & Linguraru, M. G. (2024). Enhancing generalizability in brain tumor segmentation: Model ensemble with adaptive post-processing. In *2024 IEEE International Symposium on Biomedical Imaging (ISBI)* (pp. 1-4). IEEE. https://doi.org/10.1109/ISBI56570.2024.10635469

## Disclaimer
This software is provided without any warranties or liabilities and is intended for research purposes only. It has not been approved for clinical diagnostic use by any medical device regulatory agency.

## Authors
- **Biomedical Image Technologies, Universidad Politécnica de Madrid (BIT-UPM)**
- **Pediatric Accelerated Intelligence Lab, Sheikh Zayed Institute for Pediatric Surgical Innovation, Children's National Hospital**
