FROM aparida12/brats2025:men

# EUCAIM Metadata Labels
LABEL org.opencontainers.image.title="Intracranial Meningioma Segmenter"
LABEL org.opencontainers.image.description="Inference engine for Intracranial Meningioma MRI Segmentation (BraTS 2025)"
LABEL org.opencontainers.image.authors="Universidad Politécnica de Madrid & Children's National Hospital Team"
LABEL org.opencontainers.image.source="https://github.com/BIT-UPM/EUCAIM/tree/main/intercranial_meningioma_segmenter"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.vendor="EUCAIM"

# Create input/output directories and set permissions
USER root
RUN mkdir -p /input /output && \
    chmod 777 /input /output && \
    chmod -R 777 /project

# Create a non-root user
RUN useradd -m -u 1000 appuser

# Switch to non-root user
USER appuser

ENV LANG=C.UTF-8
ENV PYTHONPATH=/project
ENV PYTHONUNBUFFERED=1

# Entrypoint
CMD ["python", "runner.py", "-i", "/input", "-o", "/output", "-t", "MEN"]
