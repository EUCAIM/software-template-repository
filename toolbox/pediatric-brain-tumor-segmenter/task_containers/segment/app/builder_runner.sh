# Define an array of tasks
tasks=("met" "men" "menrt" "peds")

# Iterate over the tasks array
for task in "${tasks[@]}"; do
    echo "Pruning Docker system before building image for task: $task"
    docker system prune -f

    if [[ "$task" == "menrt" ]]; then
        path=/media/abhijeet/DataThunder2/BraTS2025/Task3-MENRT/docker_test/
    else
        path=/media/abhijeet/DataThunder2/BraTS2025/Task2-MEN/ASNR-MICCAI-BraTS2023-MEN-Challenge-TrainingData/docker_test/
    fi
    echo "Building Docker image for task: $task"
    
    # Build the Docker image for the current task
    docker build -t aparida12/brats2025:$task -f Dockerfile_$task .

    echo "Running Docker container for task: $task"
    
    # Run the Docker container for the current task
    docker run \
        --rm \
        --network none \
        --gpus=all \
        -v $path:/input/:ro  \
        -v /media/abhijeet/DataThunder2/BraTS2025/Task2-MEN/ASNR-MICCAI-BraTS2023-MEN-Challenge-TrainingData/docker_test_out/:/output/:rw  \
        --memory=16G --shm-size 4G \
        aparida12/brats2025:$task >> $task.log

    echo "Pushing Docker image for task: $task"
    docker system prune -f
    
    # Push the Docker image for the current task
    docker push aparida12/brats2025:$task
done

for task in "${tasks[@]}"; do
    echo "Copying Docker system for task: $task"
    skopeo copy docker://docker.io/aparida12/brats2025:$task docker://docker.synapse.org/syn68174737/brats2025:$task
done