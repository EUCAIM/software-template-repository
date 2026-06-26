#!/usr/bin/env python3

import os
import json
import logging
import argparse

from aggregator import load_stats, detect_imbalance
from report import generate_html_report

# Configure logger to output to STDOUT (EUCAIM requirement)
logger = logging.getLogger("federated_unbalance_checker")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def run_aggregator(input_paths, output_path):
    logger.info(f"Aggregating results from: {input_paths}")
    stats_list = load_stats(input_paths)
    report_json = detect_imbalance(stats_list)
    with open(os.path.join(output_path, "report.json"), "w") as f:
        json.dump(report_json, f, indent=2)
    logger.info(f"Aggregator output (report.json) saved to: {output_path}")
    generate_html_report(os.path.join(output_path, "report.html"), report_json, stats_list)
    logger.info(f"Aggregator output (report.html) saved to: {output_path}")

def main():

    parser = argparse.ArgumentParser(description="Federated Unbalance Checker Aggregator")

    parser.add_argument("-i", "--input", required=True, nargs="+", help="List of runner output JSONs (paths relative to DATA_PATH if not absolute)")
    parser.add_argument("-o", "--output", required=True, help="Path to aggregated output JSON (relative to DATA_PATH if not absolute)")

    args = parser.parse_args()

    run_aggregator(args.input, args.output)

if __name__ == "__main__":
    main()
