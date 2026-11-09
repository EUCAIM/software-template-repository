from pathlib import Path
from typing import List, Union, Optional
import os
import time
import argparse
import numpy as np
import pandas as pd
import nibabel as nib
import cc3d
import warnings
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from fops.load_store import maybe_make_dir, load_json, save_json, maybe_remove_dir

    

def extract_feature(paramfile, data_path, seg_path, pid, seq, region='wt', tmpp='.'):
    img_path = data_path / f"{pid}{seq}.nii.gz"
    tmp_path = maybe_make_dir(tmpp) / f"{pid}{seq}.json"
    cmd = f"pyradiomics '{str(img_path)}' '{str(seg_path)}' -o '{str(tmp_path)}' -f json --param '{str(paramfile)}'"
    os.system(cmd)
    # load features
    new_dict = {'StudyID': pid}
    dt = load_json(tmp_path)
    tmp_path.unlink()
    # rename features
    old_dict = dt[0]
    for k in old_dict.keys():
        if k.startswith('original_shape_'):
            new_k = k.replace('original_shape_', f'{region}_shape_', 1)
            new_dict[new_k] = old_dict[k]
        elif k.startswith('original_'):
            new_k = k.replace('original_', f'{region}{seq.replace("-","_")}_', 1)
            new_dict[new_k] = old_dict[k]

    return new_dict


def extract_case(paramfile, data_path, seg_path, pid, region='wt', tmpp='.', sequences=['-t1n', '-t1c', '-t2w', '-t2f']):
    # sequences = ['t1n', 't1c', 't2w', 't2f']
    new_dict = {}
    for i, seq in enumerate(sequences):
        feature = extract_feature(paramfile, data_path, seg_path, pid, seq, region, tmpp)
        # if seq in ['-t1n','_t1n'] or len(sequences)==1:
        if i == 0:
            for k in feature.keys():
                new_dict[k] = feature[k]
        else:
            for k in feature.keys():
                if not (k.startswith('StudyID') or k.startswith(f'{region}_shape')):
                    new_dict[k] = feature[k]
    return new_dict


def create_dilation(seg_path, out_path, dilation_factor=3, region='wt'):
    img_obj = nib.load(seg_path)
    img_data = img_obj.get_fdata()
    if region == 'wt':
        binary_seg = np.where(img_data > 0, 1, 0)
    else:
        warnings.warn(f"Invalid region: {region} Compute whole tumor instead.")
        binary_seg = np.where(img_data > 0, 1, 0)
    # dilation_struct = generate_binary_structure(3, 1)
    # dilated_seg = binary_dilation(binary_seg, structure=dilation_struct, iterations=dilation_factor)

    labels_out, n = cc3d.connected_components(binary_seg, connectivity=26, return_N=True)
    vol_max = 0
    label_max = 0
    # vol_s = []
    for i in range(n):
        tmp = np.where(labels_out == i+1, 1, 0)
        vol = np.count_nonzero(tmp)
        if vol > vol_max:
            vol_max = vol
            label_max = i+1
        # vol_s.append(vol)

    dilated_seg = np.where(labels_out == label_max, 1, 0)
    seg_obj = nib.Nifti1Image(dilated_seg.astype(np.int8), img_obj.affine)
    nib.save(seg_obj, out_path)
    
    
def process_case(case: str, paramfile: Union[str, Path], data_path: Path, seg_dir: Path,
                 dilation_factor: int, region: str, tmpp: str, seg_suffix: str, sequences: List[str]) -> dict:
    try:
        seg_path = seg_dir / f"{case}{seg_suffix}.nii.gz"
        dilated_seg_path = maybe_make_dir(tmpp) / f"{case}_{region}_dilated.nii.gz"
        create_dilation(seg_path, dilated_seg_path, dilation_factor, region)
        features = extract_case(paramfile, data_path / case, dilated_seg_path, case, region, tmpp, sequences)
        dilated_seg_path.unlink(missing_ok=True)
        return features
    except Exception as e:
        print(f"Error processing case {case}: {e}")
        return {}


def extract_all(paramfile, data_path, seg_dir, output_path, dilation_factor=3, region='wt', tmpp='.',
                seg_suffix='-seg', sequences=['-t1n', '-t1c', '-t2w', '-t2f'], max_workers: Optional[int] = None):
    cases = sorted(os.listdir(data_path))
    maybe_make_dir(tmpp)
    
    features = []
    t0 = time.time()
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_case, case, paramfile, data_path, seg_dir,
                            dilation_factor, region, tmpp, seg_suffix, sequences): case
            for case in cases
        }

        for i, future in enumerate(tqdm(as_completed(futures), total=len(futures))):
            case = futures[future]
            try:
                result = future.result()
                if result:
                    features.append(result)
            except Exception as exc:
                print(f"{case} generated an exception: {exc}")

            elapsed = (time.time() - t0) / 60.0
            print(f"{i+1:04d} {case} extraction time: {elapsed:.1f} min")

        #save_json(output_path, features)
    return pd.DataFrame(features)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", type=str)
    parser.add_argument("-is", "--input-seg-dir", type=str)
    parser.add_argument("-o", "--output", type=str)
    parser.add_argument("-d", "--dilation", type=int)
    parser.add_argument("-r", "--region", type=str)
    parser.add_argument("-p", "--param", type=str)
    parser.add_argument("-t", "--tmpp", default='./tmp', type=str)
    parser.add_argument("-s", "--seg-suffix", default='-seg', type=str)
    parser.add_argument("-seq", "--sequences", nargs='+', default=['-t1n', '-t1c', '-t2w', '-t2f'])
    parser.add_argument("--num_workers", type=int, default=12, help="Number of parallel workers")
    args = parser.parse_args()
    
    print(f"Arguments: {args}")
    
    maybe_make_dir(args.tmpp)
    # from dir ./dsd/try.json to ./dsd/
    args.param = Path(args.param)
    maybe_make_dir(Path(args.output).parent)

    extract_all(
        args.param, 
        Path(args.input_dir),
        Path(args.input_seg_dir),
        args.output, 
        dilation_factor=args.dilation, 
        region=args.region,
        tmpp=args.tmpp,
        seg_suffix=args.seg_suffix,
        sequences=args.sequences,
        max_workers=args.num_workers)
    
    maybe_remove_dir(args.tmpp)