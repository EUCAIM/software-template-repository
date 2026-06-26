#!/usr/bin/env python3

import os
import random
import pandas as pd
import uuid

random.seed(42)

BASE_DIR = "./"

DATASETS = {
    "ds-1": {
        "n": 30,
        "age_range": (70, 90),
        "sex": ["COM1001366", "COM1001370"],   # ["Male", "Female"],
        "ethnicity": ["COM1001311", "COM1001046"]   #["Caucasian", "African"]
    },
    "ds-2": {
        "n": 20,
        "age_range": (20, 40),
        "sex": ["COM1001366", "COM1001370"],
        "ethnicity": ["COM1001311"]   # ["Caucasian"]
    },
    "ds-3": {
        "n": 15,
        "age_range": (30, 60),
        "sex": ["COM1001370"],
        "ethnicity": ["COM1001320"]   # ["Asian"]
    },
    "ds-4": {
        "n": 25,
        "age_range": (30, 60),
        "sex": ["COM1001366"],
        "ethnicity": ["COM1001209"]   # ["Hispanic"]
    },
    "ds-5": {
        "n": 10,
        "age_model": "normal",
        "age_params": {"mean": 60, "std": 8, "low": 40, "high": 80},
        "sex": ["COM1001366", "COM1001370"],
        "ethnicity": ["COM1001209", "COM1001311"]   # ["Hispanic", "Caucasian"]
    },
    "ds-6": {
        "n": 15,
        "age_model": "normal",
        "age_params": {"mean": 50, "std": 10, "low": 20, "high": 75},
        "sex": ["COM1001366", "COM1001370"],
        "ethnicity": ["COM1001320", "COM1001311"]   # ["Asian", "Caucasian"]
    },
    "ds-7": {
        "n": 35,
        "age_model": "normal",
        "age_params": {"mean": 55, "std": 12, "low": 25, "high": 90},
        "sex": ["COM1001366", "COM1001370"],
        "ethnicity": ["COM1001311", "COM1001046", "COM1001320", "COM1001209"]   # ["Caucasian", "African", "Asian", "Hispanic"]
    },
    "ds-8": {
        "n": 20,
        "age_pattern": "bimodal",
        "age_bins": [(20, 25), (75, 80)],
        "sex": ["COM1001366", "COM1001370"],
        "ethnicity":  ["COM1001311", "COM1001046"]   # ["Caucasian", "African"]
    }
}

def balanced_list(values, n):
    """Repeat values evenly to reach length n."""
    base = n // len(values)
    remainder = n % len(values)
    lst = []
    for v in values:
        lst.extend([v] * base)
    lst.extend(values[:remainder])
    random.shuffle(lst)
    return lst


def truncated_normal(mean, std, low, high, n):
    ages = []
    while len(ages) < n:
        x = random.gauss(mean, std)
        if low <= x <= high:
            ages.append(int(round(x)))
    return ages


def generate_ages(spec):
    n = spec["n"]

    if spec.get("age_pattern") == "bimodal":
        ages = []
        bins = spec["age_bins"]
        half = n // len(bins)
        for lo, hi in bins:
            ages.extend(random.randint(lo, hi) for _ in range(half))
        return ages

    if spec.get("age_model") == "normal":
        p = spec["age_params"]
        return truncated_normal(
            mean=p["mean"],
            std=p["std"],
            low=p["low"],
            high=p["high"],
            n=n
        )

    # fallback (uniform)
    return [random.randint(*spec["age_range"]) for _ in range(n)]


def eucaim_schema():
    mandatory_fields = {
    "diagnostic_categories": ['COM1001086', 'COM1001087', 'COM1002624', 'COM1002625', 'COM1002626', 'COM1002628'],
    "treatment_types": ['CLIN1034187', 'CLIN1035100', 'CLIN1014763', 'CLIN1014764', 'CLIN1034262', 
                      'CLIN1049098', 'CLIN1014933', 'CLIN1004413', 'CLIN1034674', 'CLIN1010523'],
    "procedure_codes": ['CLIN1000242', 'CLIN1000243', 'CLIN1000248', 'CLIN1001712', 'CLIN1001713',
                       'CLIN1001714', 'CLIN1001715', 'CLIN1001716', 'CLIN1001717', 'CLIN1001718'],
    "cancer_condition_topographies": ['BP1000021', 'BP1000051', 'BP1000075', 'BP1000142', 'BP1000192', 'BP1000209', 
                                     'BP1000286', 'BP1000290', 'BP1000291', 'BP1000298', 'BP1000299', 'BP1000301'],
    "cancer_condition_histology_morphologies": ['CLIN1000061', 'CLIN1000063', 'CLIN1000066', 'CLIN1000067', 'CLIN1000069',
                                               'CLIN1000073', 'CLIN1000081', 'CLIN1000082', 'CLIN1000113', 'CLIN1000132'],
    "cancer_condition_codes": ['CLIN1000045', 'CLIN1000053', 'CLIN1000054', 'CLIN1000057', 'CLIN1000058',
                              'CLIN1000060', 'CLIN1000062', 'CLIN1000065', 'CLIN1000068', 'CLIN1000071']}
    return mandatory_fields


def generate_dataset(name, spec):
    n = spec["n"]

    ages = generate_ages(spec)
    sexes = balanced_list(spec["sex"], n)
    ethnicities = balanced_list(spec["ethnicity"], n)
    clinical_fields = eucaim_schema()    

    df = pd.DataFrame({
        "cancer_condition_age_at_diagnosis": ages,
        "patient_birth_sex": sexes,
        "patient_ethnicity": ethnicities,

        "dataset_id": [name for _ in range(n)],
        "patient_id": [uuid.uuid4().hex for _ in range(n)],
        "patient_diagnostic_category": [random.choice(clinical_fields["diagnostic_categories"]) for _ in range(n)],
        "first_treatment_type": [random.choice(clinical_fields["treatment_types"]) for _ in range(n)],   #"treatment_type" in EUCAIM CDM Data Dictionary: https://eucaim-cdm.ics.forth.gr/
        "evidence_procedure_code": [random.choice(clinical_fields["procedure_codes"]) for _ in range(n)],   #"procedure_code" in EUCAIM CDM Data Dictionary
        "cancer_condition_type": [random.choice(['COM1000017', 'COM1000159']) for _ in range(n)],
        "cancer_condition_topography": [random.choice(clinical_fields["cancer_condition_topographies"]) for _ in range(n)],
        "cancer_condition_histology_morphology": [random.choice(clinical_fields["cancer_condition_histology_morphologies"]) for _ in range(n)],
        "cancer_condition_code": [random.choice(clinical_fields["cancer_condition_codes"]) for _ in range(n)],
        "cancer_condition_age_unit": ['COM1000151' for _ in range(n)]
    })

    out_dir = os.path.join(BASE_DIR, name)
    os.makedirs(out_dir, exist_ok=True)
    df.to_csv(os.path.join(out_dir, "clinical_mandatory_view.csv"), index=False)

    print(f"Generated {name}: {n} patients")

def main():
    for name, spec in DATASETS.items():
        generate_dataset(name, spec)

if __name__ == "__main__":
    main()

