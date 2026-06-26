#!/usr/bin/env python3

import os
import sys
import json
import pandas as pd
from collections import Counter
import statistics as stats
# from eucaim_cdm_reader import CdmReader


def load_eucaim(dataset_path):
    # Try to load the dataset as EUCAIM CDM and EUCAIM FS format (clinical_mandatory_view.csv)
    loaded = False
    try:
        df = pd.read_csv(os.path.join(dataset_path, "clinical_mandatory_view.csv"))
        # df = CdmReader(dataset_path).mandatory_clinical_data
        summary = {
            "dataset_id": df['dataset_id'].iloc[0],
            "num_patients": len(df),
            "age_mean": df['cancer_condition_age_at_diagnosis'].mean(),
            "age_std": df['cancer_condition_age_at_diagnosis'].std(),
            "sex_counts": df['patient_birth_sex'].value_counts().to_dict(),
            "ethnicity_counts": df['patient_ethnicity'].value_counts().to_dict(),
            "exitcode": 0,
            "error": None
        }
        loaded = True
    except Exception as e:
        summary = {
            "dataset_id": os.path.splitext(os.path.basename(dataset_path))[0],
            "num_patients": None,
            "age_mean": None,
            "age_std": None,
            "sex_counts": None,
            "ethnicity_counts": None,
            "exitcode": 1,
            "error": str(e)
        }
    return loaded, summary


def load_chaimeleon(dataset_path):
    # Try to load the dataset as ChAImeleon format (eforms.json)
    loaded = False
    try:
        eforms_file_path = os.path.join(dataset_path, "eforms.json")
        with open(eforms_file_path) as fr:
            ds = json.load(fr)
        
        summary = {
            "dataset_id": os.path.splitext(os.path.basename(dataset_path))[0],
            "num_patients": len(ds),
            "age_mean": stats.mean([x['eForm']['pages'][0]['page_data']['age_at_diagnosis']['value'] for x in ds]), # inclusion_criteria
            "age_std": stats.stdev([x['eForm']['pages'][0]['page_data']['age_at_diagnosis']['value'] for x in ds]), # inclusion_criteria
            "sex_counts": Counter([x['eForm']['pages'][1]['page_data']['gender']['value'] for x in ds]), # patien_data
            "ethnicity_counts": None,
            "exitcode": 0,
            "error": None
        }
        loaded = True
    
    except Exception as e:
        summary = {
            "dataset_id": os.path.splitext(os.path.basename(dataset_path))[0],
            "num_patients": None,
            "age_mean": None,
            "age_std": None,
            "sex_counts": None,
            "ethnicity_counts": None,
            "exitcode": 1,
            "error": str(e)
        }
    
    return loaded, summary


def compute_statistics(dataset_path):
    # First try to load as EUCAIM, if it fails, try to load as ChAImeleon. 
    type = "ecuaim"
    flag, stats = load_eucaim(dataset_path)
    if not flag:
        type = "chaimeleon"
        flag, stats = load_chaimeleon(dataset_path)
    stats["dataset_type"] = type
    return stats
    

if __name__ == "__main__":
    dataset_path = sys.argv[1] # Path to local dataset
    output_path = sys.argv[2]  # Where to store the output JSON
    
    stats = compute_statistics(dataset_path)
    
    with open(output_path, 'w') as fw:
        json.dump(stats, fw, indent = 2)
    
    print(f"Processed {dataset_path} and saved stats to {output_path}")
    