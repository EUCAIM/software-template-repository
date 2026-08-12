#!/usr/bin/env bash
# EUCAIM onboarding test for the nnU-Net Brain Tumour PET container.
# Usage: bash test/run_eucaim_onboarding_test.sh
#
# This tool requires a representative static 18F-FET PET DICOM test case.
# At present, no suitable redistributable test fixture has been included.
#
# Once an approved test input and corresponding reference output are available,
# replace this status check with the standard container onboarding runner.
set -euo pipefail

# Report the test status.
echo "[nnU-Net Brain Tumour PET] Test blocked."
echo "[nnU-Net Brain Tumour PET] No approved static 18F-FET PET test fixture is currently available."
echo "[nnU-Net Brain Tumour PET] An approved DICOM input and reference output are required before this onboarding test can be executed."

exit 1