# Test input

The onboarding runner creates its virtual environment and downloads the fixed
`StageII-Colorectal-CT-010` CT series here when needed. The DICOM files are
ignored by Git. Its pinned identifiers, licence and validation requirements are
in [`../test_dataset.yaml`](../test_dataset.yaml).

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
