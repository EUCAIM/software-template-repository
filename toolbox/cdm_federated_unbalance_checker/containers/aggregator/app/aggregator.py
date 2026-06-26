#!/usr/bin/env python3

import json
import sys
import pandas as pd

def load_stats(json_paths):
    return [json.load(open(path)) for path in json_paths]

def detect_imbalance(stats_list, age_threshold = 15, min_frac = 0.3, client_dominance = 0.9):
    # Filteting out the invalid datasets
    n1 = len(stats_list)
    valid = [x for x in stats_list if x.get('exitcode') == 0]
    n2 = len(valid)

    df = pd.DataFrame(valid)

    # Age imbalance
    age_imbalance = False
    age_diff = None
    if 'age_mean' in df and df['age_mean'].notna().any():
        age_means = df['age_mean'].dropna()
        age_diff = age_means.max() - age_means.min()
        age_imbalance = bool(age_diff > age_threshold)

    # Helper: global + client-aware imbalance
    def categorical_global_imbalance(field):
        total_counts = {}
        client_degenerate = []

        for s in valid:
            counts = s.get(field)
            if counts is None:
                continue
            
            if not counts:
                continue

            total = sum(counts.values())
            if total == 0:
                continue

            # accumulate global
            for k, v in counts.items():
                total_counts[str(k).lower()] = total_counts.get(str(k).lower(), 0) + v

            # check client degeneracy
            dominant_frac = max(counts.values()) / total
            if dominant_frac >= client_dominance:
                client_degenerate.append(s["dataset_id"])

        if not total_counts:
            return False, {}

        global_total = sum(total_counts.values())
        global_dom_frac = max(total_counts.values()) / global_total

        global_skew = global_dom_frac > (1 - min_frac)
        global_imbalance = global_skew or bool(client_degenerate)

        return global_imbalance, {
            "global_counts": total_counts,
            "global_dominant_frac": global_dom_frac,
            "degenerate_clients": client_degenerate
        }

    sex_imbalance, sex_details = categorical_global_imbalance("sex_counts")
    eth_imbalance, eth_details = categorical_global_imbalance("ethnicity_counts")

    # Aggregated Results
    report = {
        "age_imbalance": age_imbalance,
        "sex_imbalance": sex_imbalance,
        "ethnicity_imbalance": eth_imbalance,
        "details": {
            "sex": sex_details,
            "ethnicity": eth_details
        },
        "age_diff": age_diff,
        "number_sets": n1,
        "evaluated_sets": n2
    }

    return report

if __name__ == "__main__":
    json_paths = sys.argv[1:]  # Paths to all JSON stats
    stats_list = load_stats(json_paths)
    report = detect_imbalance(stats_list)
    print("Imbalance Report:")
    for k, v in report.items():
        print(f"- {k}: {v}")
        