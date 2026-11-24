# Expected Output Description: Pediatric Brain Tumor Segmenter

## Output File Format & Organization
The tool processes the input MRI modalities and writes a single 3D compressed NIfTI mask file corresponding to each evaluated study directly into the output directory:

```text
example_output/
├── BraTS-PED-00030-000.nii.gz
└── description.md
```

### Volume Specifications
- **Format:** NIfTI-1 compressed (`.nii.gz`)
- **Matrix Dimensions:** 240 × 240 × 155 voxels
- **Voxel Spacing:** 1.0 mm × 1.0 mm × 1.0 mm (isotropic SRI24 anatomical space)
- **Data Type:** Integer / Floating-point discrete segmentation map

### Label Definitions (BraTS-PED (Pediatric Brain Tumors))
- `0`: Background
- `1`: Enhancing tumor (ET)
- `2`: Non-enhancing tumor (NET)
- `3`: Cystic component (CC)
- `4`: Peritumoral edema (ED)

## Non-Determinism & Integration Validation
Deep learning inference involving cuDNN, matrix multiplication optimizations, and multi-threaded CPU preprocessing can produce minor floating-point differences across different GPU architectures (e.g., Ampere vs. Ada Lovelace vs. Hopper) or driver versions.

### Validation Criteria
During EUCAIM platform integration testing, an output is considered **valid** if:
1. **File Existence:** The expected output file (`BraTS-PED-00030-000.nii.gz`) is successfully generated in the output directory and non-empty.
2. **Header & Geometry:** Spatial dimensions (`240, 240, 155`), affine orientation matrix, and spacing match the input volume.
3. **Segmentation Consistency:** The Dice similarity coefficient between the freshly computed output and the reference mask in `example_output/` satisfies:
   $$\text{Dice} \ge 0.99$$
