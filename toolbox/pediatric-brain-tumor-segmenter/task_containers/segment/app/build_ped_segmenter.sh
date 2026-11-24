#!/bin/bash

# Check if weight files exist
if [ ! -f "./weights/BraTS2025-PED_nnUNetv2_model.zip" ] || \
   [ ! -f "./weights/BraTS2025-PED_MedNeXt_model.zip" ] || \
   [ ! -f "./weights/BraTS2025-PED_nnUNetv2-ResEnc_model.zip" ]; then
    echo "Error: Missing model weight zip files in ./weights/"
    echo "Please ensure the following files are present:"
    echo "  - ./weights/BraTS2025-PED_nnUNetv2_model.zip"
    echo "  - ./weights/BraTS2025-PED_MedNeXt_model.zip"
    echo "  - ./weights/BraTS2025-PED_nnUNetv2-ResEnc_model.zip"
    exit 1
fi

# Build the Docker image
docker build -t eucaim/brats2025-ped-segmenter:v1.0.0 -f Dockerfile.eucaim .

echo "Build complete. Run with:"
echo "docker run --rm --gpus all -v /path/to/input:/input -v /path/to/output:/output eucaim/brats2025-ped-segmenter:v1.0.0"
