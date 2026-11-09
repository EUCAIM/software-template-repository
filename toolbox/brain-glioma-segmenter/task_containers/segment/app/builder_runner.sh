echo "Pruning Docker system before building image for task"
docker system prune -f
echo "Building Docker image for task"
docker build -t aparida12/brats2025:gli -f Dockerfile .
echo "Running Docker container for task"
docker run \
        --rm \
        --network none \
        --gpus=all \
        -v /media/abhijeet/DataThunder2/BraTS2025/Task1-GLI/docker_test/:/input/:ro  \
        -v /media/abhijeet/DataThunder2/BraTS2025/Task2-MEN/ASNR-MICCAI-BraTS2023-MEN-Challenge-TrainingData/docker_test_out/:/output/:rw  \
        --memory=16G --shm-size 4G \
        aparida12/brats2025:gli > gli_infer_log.txt
echo "Pushing Docker image for task"
docker system prune -f
docker push aparida12/brats2025:gli
skopeo copy docker://docker.io/aparida12/brats2025:gli docker://docker.synapse.org/syn68174737/brats2025:gli

