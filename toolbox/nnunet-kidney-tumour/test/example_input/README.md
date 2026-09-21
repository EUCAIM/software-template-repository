# Test input

The onboarding runner creates its virtual environment and downloads the fixed
series recorded in [`../test_dataset.yaml`](../test_dataset.yaml) here when
needed. The DICOM files are ignored by Git; identifiers and validation
requirements are in that file.

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
