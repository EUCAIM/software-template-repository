# Integration-test input: Pancreas-CT `PANCREAS_0080`

This directory contains the fixed input for EUCAIM integration validation. The
public TCIA DICOM files are downloaded on demand and are not committed to Git.
The onboarding runner creates its virtual environment and prepares this input
automatically:

```bash
bash toolbox/nnunet-pancreas-tumour/test/run_eucaim_onboarding_test.sh
```

The downloader can also be run directly for fixture preparation after
installing `test/requirements.txt` manually.

This creates the complete CT series required by `Task007_Pancreas`:

```text
example_input/
└── PANCREAS_0080/
    ├── 000001.dcm
    └── ...
```

The downloader is intentionally pinned to one patient, study, and
SeriesInstanceUID. It verifies 181 CT instances, consistent geometry, and the
absence of DICOM SEG or RTSTRUCT input objects before accepting the download.

See [DATA_LICENSE.md](DATA_LICENSE.md) for collection provenance, license,
required citations, and the fixed identifiers.
