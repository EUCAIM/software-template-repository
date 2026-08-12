# EUCAIM onboarding test

`run_eucaim_onboarding_test.sh` is the reproducible smoke test for the
registered hippocampus image. It uses the committed derived DICOM MR series
and never changes either fixture.

## Prerequisites and run

Docker or Podman with one CUDA-capable GPU, Python 3, and network access to
the EUCAIM Harbor registry are required. From the repository root, run:

```bash
bash toolbox/nnunet-hippocampus-segmentation/test/run_eucaim_onboarding_test.sh
```

The runner creates or reuses `.venv_onboarding`, pulls the registered Harbor
image, mounts `example_input/` read-only, writes to `actual_output/`, and
fails unless the container creates at least one output file. `actual_output/`
is ignored by Git; `example_output/` remains the committed reference.

## Local folder example

A complete repository-level local test is available under
`local_test/nnunet-hippocampus/`. It includes its own input and wrapper runner:

```bash
bash local_test/nnunet-hippocampus/run_eucaim_onboarding_test.sh
```

The folder must contain immediate child directories, one per DICOM series.

## Optional paths

Supported variables are `CONTAINER_RUNTIME=docker|podman`, `INPUT_DIR`,
`OUTPUT_DIR`, and `VENV_DIR`. Syntax can be checked with:

```bash
bash -n toolbox/nnunet-hippocampus-segmentation/test/run_eucaim_onboarding_test.sh
```
