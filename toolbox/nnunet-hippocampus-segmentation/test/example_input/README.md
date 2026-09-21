# Test input

This directory holds a committed derived DICOM MR series for the
hippocampus onboarding test. It was prepared from the public Medical
Segmentation Decathlon Task04 source image
`imagesTr/hippocampus_001.nii.gz`.

The series is a derived test artifact, not an original clinical DICOM
acquisition. Its source checksum, licence, conversion summary, and fixed DICOM
identifiers are recorded in [`../test_dataset.yaml`](../test_dataset.yaml) and
[`DATA_LICENSE.md`](DATA_LICENSE.md).

The data is laid out in the EUCAIM CDM/FS structure, matching what the
materialisor delivers on the platform:

```text
example_input/
└── dataset/
    └── imaging_data/
        └── {patient_id}/
            └── {study_uid}/
                └── {series_uid}/
                    └── *.dcm
```
