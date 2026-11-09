# Test Dataset Notice (Intracranial Meningioma Segmenter (BraTS-MEN))

## Data Provenance & Terms of Use
The sample MRI volume provided in `test/example_input/` is strictly intended for technical integration testing, unit verification, and CI/CD validation within the EUCAIM platform. The imaging data originates from the Brain Tumor Segmentation (BraTS) Challenge benchmarks organized under the auspices of MICCAI and Sage Bionetworks (Synapse).

Use, distribution, or reproduction of BraTS data beyond technical integration testing requires registration and adherence to the official BraTS Data Use Agreement at [synapse.org](https://www.synapse.org/brats). This data is strictly for Research Use Only (RUO).

### File Layout
This folder contains 1 representative study structured according to the BraTS and EUCAIM Common Data Model (CDM):
- `*-t1n.nii.gz`: T1-weighted native
- `*-t1c.nii.gz`: T1-weighted post-contrast
- `*-t2w.nii.gz`: T2-weighted
- `*-t2f.nii.gz`: T2-weighted FLAIR

Dimensions: 240 × 240 × 155 voxels at 1.0 mm³ isotropic spacing (SRI24 atlas space).
