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

def run_runner(input_path, output_path):
    logger.info(f"Running runner on dataset: {input_path}")
    stats = compute_statistics(input_path)
    with open(output_path, "w") as f:
        json.dump(stats, f, indent=2)
    logger.info(f"Runner output saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Federated Unbalance Checker Runner")
    
    parser.add_argument("-i", "--input", required=True, help="Path to dataset CSV (relative to DATA_PATH if not absolute)")
    parser.add_argument("-o", "--output", required=True, help="Path to output JSON (relative to DATA_PATH if not absolute)")
    
    args = parser.parse_args()
    
    run_runner(args.input, args.output)

if __name__ == "__main__":
    main()
