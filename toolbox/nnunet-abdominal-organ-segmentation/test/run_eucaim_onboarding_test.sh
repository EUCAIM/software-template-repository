#!/usr/bin/env bash
# Purpose: Run the fixed abdominal-organ EUCAIM onboarding smoke test.
# Usage:   bash test/run_eucaim_onboarding_test.sh
#
# Prerequisites: Docker or Podman, a CUDA-capable GPU, Python 3, TCIA network
# access for the first input download, and Harbor access/authentication.
#
# The script creates/reuses VENV_DIR, installs test/requirements.txt once,
# reuses or downloads the pinned input, pulls the registered image, runs it,
# and requires at least one output file. It never overwrites fixtures.
#
# Optional variables: CONTAINER_RUNTIME, INPUT_DIR, OUTPUT_DIR, VENV_DIR.
# EUCAIM onboarding test for the registered abdominal-organ-segmentation container.
# Run this script from any working directory.
set -euo pipefail

# Resolve paths and configuration.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTAINER_RUNTIME="${CONTAINER_RUNTIME:-docker}"
APP_IMAGE="harbor.eucaim.cancerimage.eu/processing-tools/nnunet-abdominal-organ-segmentation:1.0.0"
INPUT_DIR="${INPUT_DIR:-${SCRIPT_DIR}/example_input}"
OUTPUT_DIR="${OUTPUT_DIR:-${SCRIPT_DIR}/actual_output}"
VENV_DIR="${VENV_DIR:-${SCRIPT_DIR}/.venv_onboarding}"

log() { echo "[nnU-Net Abdominal Organ Segmentation] $*"; }
fail() { echo "[nnU-Net Abdominal Organ Segmentation] ERROR: $*" >&2; exit 1; }

# Check prerequisites and prepare the Python environment.
command -v "${CONTAINER_RUNTIME}" >/dev/null 2>&1 || fail "Container runtime not found: ${CONTAINER_RUNTIME}"
command -v python3 >/dev/null 2>&1 || fail "python3 is required"

if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
  log "Creating virtual environment: ${VENV_DIR}"
  python3 -m venv "${VENV_DIR}"
  "${VENV_DIR}/bin/python" -m pip install -r "${SCRIPT_DIR}/requirements.txt"
fi
# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

# Reuse or download the pinned input series.
log "Preparing the pinned TCIA input"
python "${SCRIPT_DIR}/download_tcia_test_data.py" \
  --config "${SCRIPT_DIR}/test_dataset.yaml" --output-dir "${INPUT_DIR}"
[[ -n "$(find "${INPUT_DIR}" -mindepth 1 -maxdepth 1 -type d -print -quit)" ]] \
  || fail "No DICOM series found in ${INPUT_DIR}"

# Select the GPU option for the chosen runtime.
case "${CONTAINER_RUNTIME}" in
  docker) GPU_ARGS=(--gpus all) ;;
  podman) GPU_ARGS=(--device nvidia.com/gpu=all) ;;
  *) fail "Unsupported runtime ${CONTAINER_RUNTIME}; use docker or podman" ;;
esac

# Pull the registered Harbor image.
log "Pulling image: ${APP_IMAGE}"
"${CONTAINER_RUNTIME}" pull "${APP_IMAGE}"

# Prepare an empty output directory.
mkdir -p "${OUTPUT_DIR}"
[[ -z "$(find "${OUTPUT_DIR}" -mindepth 1 -print -quit)" ]] || fail "Output directory must be empty: ${OUTPUT_DIR}"

# Run the container with read-only input and writable output mounts.
log "Running image with input ${INPUT_DIR}"
"${CONTAINER_RUNTIME}" run --rm \
  "${GPU_ARGS[@]}" \
  -e "HOST_UID=$(id -u)" -e "HOST_GID=$(id -g)" \
  -v "${INPUT_DIR}:/home/eucaim/nnUNet_input:ro" \
  -v "${OUTPUT_DIR}:/home/eucaim/nnUNet_output" \
  "${APP_IMAGE}"

# Confirm that the container produced a result.
[[ -n "$(find "${OUTPUT_DIR}" -type f -print -quit)" ]] || fail "The container completed without creating an output file"
log "PASSED. Output: ${OUTPUT_DIR}"
