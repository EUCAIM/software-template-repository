FROM aparida12/brats2025:peds

# EUCAIM Metadata Labels
LABEL org.opencontainers.image.title="Pediatric Brain Tumor Segmenter"
LABEL org.opencontainers.image.description="Inference engine for Pediatric Brain MRI Segmentation (BraTS 2025)"
LABEL org.opencontainers.image.authors="Universidad Politécnica de Madrid & Children's National Hospital Team"
LABEL org.opencontainers.image.source="https://github.com/BIT-UPM/EUCAIM/tree/main/pediatric_brain_tumor_segmenter"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.vendor="EUCAIM"

# Create input/output directories and set permissions
# We use chmod 777 to allow writing by arbitrary users (common in container platforms)
USER root
RUN mkdir -p /input /output && \
    chmod 777 /input /output && \
    chmod -R 777 /project

# Create a non-root user (optional but recommended for compliance)
RUN useradd -m -u 1000 appuser

# Switch to non-root user
USER appuser

ENV LANG=C.UTF-8
ENV PYTHONPATH=/project
ENV PYTHONUNBUFFERED=1

# Entrypoint
CMD ["python", "runner.py", "-i", "/input", "-o", "/output", "-t", "PED"]
