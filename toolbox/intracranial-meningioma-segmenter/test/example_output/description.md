# Expected Output Description: Intracranial Meningioma Segmenter

## Output File Format & Organization
The tool processes the input MRI modalities and writes a single 3D compressed NIfTI mask file corresponding to each evaluated study directly into the output directory:

```text
example_output/
├── BraTS-MEN-00000-000.nii.gz
└── description.md
```

### Volume Specifications
- **Format:** NIfTI-1 compressed (`.nii.gz`)
- **Matrix Dimensions:** 240 × 240 × 155 voxels
- **Voxel Spacing:** 1.0 mm × 1.0 mm × 1.0 mm (isotropic SRI24 anatomical space)
- **Data Type:** Integer / Floating-point discrete segmentation map

### Label Definitions (BraTS-MEN (Intracranial Meningioma))
- `0`: Background
- `2`: Surrounding non-enhancing FLAIR hyperintensity (SNFH)
- `3`: Enhancing tumor (ET)

## Non-Determinism & Integration Validation
Deep learning inference involving cuDNN, matrix multiplication optimizations, and multi-threaded CPU preprocessing can produce minor floating-point differences across different GPU architectures (e.g., Ampere vs. Ada Lovelace vs. Hopper) or driver versions.

### Validation Criteria
During EUCAIM platform integration testing, an output is considered **valid** if:
1. **File Existence:** The expected output file (`BraTS-MEN-00000-000.nii.gz`) is successfully generated in the output directory and non-empty.
2. **Header & Geometry:** Spatial dimensions (`240, 240, 155`), affine orientation matrix, and spacing match the input volume.
3. **Segmentation Consistency:** The Dice similarity coefficient between the freshly computed output and the reference mask in `example_output/` satisfies:
   $$\text{Dice} \ge 0.99$$
