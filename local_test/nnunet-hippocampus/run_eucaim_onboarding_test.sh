#!/usr/bin/env bash
# Purpose: Run the hippocampus container from a locally available image.
# Usage:   LOCAL_IMAGE=<image> bash run_eucaim_onboarding_test.sh
#
# This local test does not contact Harbor. The production onboarding runner
# remains responsible for testing the registered Harbor image.
set -euo pipefail

# Resolve paths and configuration.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTAINER_RUNTIME="${CONTAINER_RUNTIME:-docker}"
LOCAL_IMAGE="${LOCAL_IMAGE:-nnunet:Task004_Hippocampus}"
INPUT_DIR="${INPUT_DIR:-${SCRIPT_DIR}/input}"
OUTPUT_DIR="${OUTPUT_DIR:-${SCRIPT_DIR}/output}"

log() { echo "[Local nnU-Net Hippocampus] $*"; }
fail() { echo "[Local nnU-Net Hippocampus] ERROR: $*" >&2; exit 1; }

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

# Confirm that the local image exists without contacting a registry.
"${CONTAINER_RUNTIME}" image inspect "${LOCAL_IMAGE}" >/dev/null 2>&1 \
  || fail "Local image not found: ${LOCAL_IMAGE}"

# Prepare an empty output directory.
mkdir -p "${OUTPUT_DIR}"
[[ -z "$(find "${OUTPUT_DIR}" -mindepth 1 -print -quit)" ]] \
  || fail "Output directory must be empty: ${OUTPUT_DIR}"
chmod 0777 "${OUTPUT_DIR}"

# Run the local image with read-only input and writable output mounts.
log "Running local image: ${LOCAL_IMAGE}"
"${CONTAINER_RUNTIME}" run --rm \
  "${GPU_ARGS[@]}" \
  -v "${INPUT_DIR}:/home/eucaim/nnUNet_input:ro" \
  -v "${OUTPUT_DIR}:/home/eucaim/nnUNet_output" \
  "${LOCAL_IMAGE}"

# Confirm that the container produced a result.
[[ -n "$(find "${OUTPUT_DIR}" -type f -print -quit)" ]] \
  || fail "The container completed without creating an output file"
log "PASSED. Output: ${OUTPUT_DIR}"
