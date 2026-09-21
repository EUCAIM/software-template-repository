# EUCAIM onboarding test

`run_eucaim_onboarding_test.sh` is the reproducible smoke test for the
registered abdominal-organ-segmentation image. It uses the pinned series in `test_dataset.yaml`
and never changes the committed fixture or reference output.

## Prerequisites

- Docker or Podman with access to one CUDA-capable GPU.
- Python 3 with permission to create a virtual environment.
- Network access to TCIA and the EUCAIM Harbor registry. Harbor credentials
  may be requested by the container runtime.

## Run

From the repository root:

```bash
bash toolbox/nnunet-abdominal-organ-segmentation/test/run_eucaim_onboarding_test.sh
```

The runner creates or reuses `.venv_onboarding`, installs the test requirements
on first use, downloads and validates the fixed TCIA series, pulls the
registered Harbor image, runs it with the input mounted read-only, and fails
unless at least one output file is created. The first run therefore requires
network access to both TCIA and Harbor.

Generated files are written to `test/actual_output/`, which is ignored by Git.
The committed DICOM SEG in `example_output/` is a reference for review and is
never overwritten by the runner.

## Optional paths

The runner supports these environment variables:

- `CONTAINER_RUNTIME=docker|podman` (default: `docker`)
- `INPUT_DIR=/absolute/or/relative/input-directory`
- `OUTPUT_DIR=/absolute/or/relative/output-directory`
- `VENV_DIR=/absolute/or/relative/virtual-environment`

`INPUT_DIR` must contain at least one directory holding DICOM files. Both a
directory of series subdirectories and the EUCAIM CDM/FS layout are accepted,
and every directory containing `.dcm` files is processed as one series. Use a
clean output directory for every run.

Shell syntax can be checked locally:

```bash
bash -n toolbox/nnunet-abdominal-organ-segmentation/test/run_eucaim_onboarding_test.sh
```
