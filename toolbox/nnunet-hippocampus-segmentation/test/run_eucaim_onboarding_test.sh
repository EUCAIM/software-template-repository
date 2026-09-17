#!/usr/bin/env bash
# Purpose: Run the fixed hippocampus EUCAIM onboarding smoke test.
# Usage:   bash test/run_eucaim_onboarding_test.sh
#
# Prerequisites: Docker or Podman, a CUDA-capable GPU, and Harbor
# access/authentication. The script pulls the registered image, mounts
# INPUT_DIR read-only, runs it, and requires at least one output file.
# Optional variables are CONTAINER_RUNTIME, INPUT_DIR, and OUTPUT_DIR.
# The DICOM input series is committed under test/example_input/.
# EUCAIM onboarding test for the registered hippocampus container.
# Run this script from any working directory.
set -euo pipefail

# Resolve paths and configuration.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTAINER_RUNTIME="${CONTAINER_RUNTIME:-docker}"
APP_IMAGE="harbor.eucaim.cancerimage.eu/processing-tools/nnunet-hippocampus-segmentation:1.0.0"
INPUT_DIR="${INPUT_DIR:-${SCRIPT_DIR}/example_input}"
OUTPUT_DIR="${OUTPUT_DIR:-${SCRIPT_DIR}/actual_output}"

log() { echo "[nnU-Net Hippocampus Segmentation] $*"; }
fail() { echo "[nnU-Net Hippocampus Segmentation] ERROR: $*" >&2; exit 1; }

# Check prerequisites.
command -v "${CONTAINER_RUNTIME}" >/dev/null 2>&1 \
  || fail "Container runtime not found: ${CONTAINER_RUNTIME}"
[[ -d "${INPUT_DIR}" ]] || fail "Input directory is missing: ${INPUT_DIR}"

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
[[ -z "$(find "${OUTPUT_DIR}" -mindepth 1 -print -quit)" ]] \
  || fail "Output directory must be empty: ${OUTPUT_DIR}"

# Run the container with read-only input and writable output mounts.
log "Running image with input ${INPUT_DIR}"
"${CONTAINER_RUNTIME}" run --rm \
  "${GPU_ARGS[@]}" \
  -e "HOST_UID=$(id -u)" -e "HOST_GID=$(id -g)" \
  -v "${INPUT_DIR}:/home/eucaim/nnUNet_input:ro" \
  -v "${OUTPUT_DIR}:/home/eucaim/nnUNet_output" \
  "${APP_IMAGE}"

# Confirm that the container produced a result.
[[ -n "$(find "${OUTPUT_DIR}" -type f -print -quit)" ]] \
  || fail "The container completed without creating an output file"
log "PASSED. Output: ${OUTPUT_DIR}"
