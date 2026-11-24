# Data provenance and licence

`MSD-HIPP-001` is a derived DICOM MR test series created from the Medical
Segmentation Decathlon Task04_Hippocampus training image
`imagesTr/hippocampus_001.nii.gz`.

The Medical Segmentation Decathlon dataset is distributed under the
Creative Commons Attribution-ShareAlike 4.0 International licence
(CC BY-SA 4.0).

This derived DICOM series is distributed under the same licence:
https://creativecommons.org/licenses/by-sa/4.0/

Source:
https://medicaldecathlon.com/

## Modifications

The original NIfTI image was converted to a 35-slice, 1 mm isotropic DICOM MR
series using nibabel and pydicom for use as an EUCAIM integration-test input.

The resulting DICOM files are derived data and are not original scanner DICOM
objects.

Source NIfTI SHA-256:
`ab47d6115b412ffaba041cbf48962967127f199f39eb56c777a6bb3746353b4a`