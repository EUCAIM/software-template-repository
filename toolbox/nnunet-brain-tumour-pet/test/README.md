# EUCAIM onboarding test status

The runner is deliberately fail-fast because no approved public, legally
redistributable 18F-FET PET DICOM series is currently available for this tool.
Without a compliant input and reference DICOM SEG, an automated result check
would not be meaningful.

When the fixture becomes available, add the input and reference output under
this directory and extend `run_eucaim_onboarding_test.sh` using the same flow
as the other nnU-Net tools: create a small virtual environment if required,
prepare the pinned input, pull the registered Harbor image, run it with a
read-only input mount, and require a non-empty output directory.

The current status can be checked explicitly with:

```bash
bash test/run_eucaim_onboarding_test.sh
```

It exits with code 1 and explains the missing fixture; this is an unavailable
test prerequisite, not a model result.
