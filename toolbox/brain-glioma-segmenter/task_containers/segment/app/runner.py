
from pathlib import Path
import tqdm
import torch.serialization
torch.serialization.add_safe_globals(["numpy.core.multiarray.scalar"])
import torch

from mlcube_infer24 import infer as mlcube_infer24
from mlcube_infer23 import infer as mlcube_infer23

def infer(data_path, output_path):
 
    if torch.cuda.is_available():
        print("GPU is available")
    else:
        print("GPU is not available")

    # check if pre-treatment or post-treatment
    print(f"Data path: {data_path}")
    for input_path in tqdm.tqdm(Path(data_path).iterdir()):
        print(f"Input path: {input_path}")
        input_path = str(input_path)
        if input_path.split("-")[-1][0] == "0":
            print("Running pre-treatment inference")
            mlcube_infer23(
                data_path=input_path,
                output_path=output_path
            )
        else:
            print("Running post-treatment inference")
            mlcube_infer24(
                data_path=input_path,
                output_path=output_path
            )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run inference and postprocessing for BraTS2025 tasks.")
    parser.add_argument('-i', '--input', type=str, required=True, help='Input folder containing the images.')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output folder to store the results.')
    parser.add_argument('-t', '--task', type=str, required=True, help='Task name for which inference is done.')
    args = parser.parse_args()
    # unzip checkpoints if needed

    print(f"Running inference for task: {args.task}")
    infer(data_path=args.input, output_path=args.output)