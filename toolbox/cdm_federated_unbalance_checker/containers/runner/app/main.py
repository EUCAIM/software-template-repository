#!/usr/bin/env python3

import os
import json
import logging
import argparse

from runner import compute_statistics

# Configure logger to output to STDOUT (EUCAIM requirement)
logger = logging.getLogger("federated_unbalance_checker")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def run_runner(input_paths, output_path):
    if isinstance(input_paths, list):
        for input_path in input_paths:
            logger.info(f"Running runner on dataset: {input_path}")
            stats = compute_statistics(input_path)
            ds_output_path = os.path.join(output_path, stats['dataset_id'] + '_output.json')  # added the .json part to avoid the need for user to specify a name in the output path
            with open(ds_output_path, "w") as f:  
                json.dump(stats, f, indent=2)
            logger.info(f"Runner output saved to: {ds_output_path}")
    else:
        print(f"Input path is not a list: {input_paths}")
        logger.error(f"Input path is not a list: {input_paths}")

def main():
    parser = argparse.ArgumentParser(description="Federated Unbalance Checker Runner")
    
    parser.add_argument("-i", "--input", required=True, nargs="+", help="List of paths to dataset CSV files (relative to DATA_PATH if not absolute)")
    parser.add_argument("-o", "--output", required=True, help="Path to output JSON (relative to DATA_PATH if not absolute)")
    
    args = parser.parse_args()
    
    run_runner(args.input, args.output)

if __name__ == "__main__":
    main()
