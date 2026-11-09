from pathlib import Path
import numpy as np
import nibabel as nib
import os

def convert_npz_mednext(npz_path, pkl_path, save_nifti=False, nifti_dir=Path('./tmp_prob_nifti'), suffix='mednext'):
    try:
        npz = np.load(npz_path, allow_pickle=True)
    except Exception as e:
        raise RuntimeError(f"Error loading npz file {npz_path}: {e}")
    try:
        pkl = np.load(pkl_path, allow_pickle=True)
    except Exception as e:
        raise RuntimeError(f"Error loading pkl file {pkl_path}: {e}")
    prob = npz[npz.files[0]].astype(np.float32)
    bbox = pkl['crop_bbox']
    shape_original_before_cropping = pkl['original_size_of_raw_data']
    out_list = []
    for i in range(0, prob.shape[0]):
        if bbox is not None:    
            seg_old_size = np.zeros(shape_original_before_cropping, dtype=np.float16)
            for c in range(3):
                bbox[c][1] = np.min((bbox[c][0] + prob[i].shape[c], shape_original_before_cropping[c]))
            seg_old_size[bbox[0][0]:bbox[0][1], bbox[1][0]:bbox[1][1], bbox[2][0]:bbox[2][1]] = prob[i]
        else:
            seg_old_size = prob[i]
        out = np.swapaxes(seg_old_size, 0, 2)
        n_nan = np.count_nonzero(np.isnan(out))
        if n_nan > 0:
            print(f"NaN values found in {npz_path}: {n_nan}")
        out_list.append(out)
        if save_nifti:
            if not nifti_dir.exists():
                nifti_dir.mkdir(parents=True)
            nib.save(
                nib.Nifti1Image(out.astype(np.float32), affine=np.eye(4)), 
                nifti_dir / f"{npz_path.name.split('.npz')[0]}_{i}_{suffix}.nii.gz"
            )
    
    return np.stack(out_list, axis=0).astype(np.float32)

def convert_npz_nnunet(npz_path, save_nifti=False, nifti_dir=Path('./tmp_prob_nifti'), suffix='nnunet'):
    try:
        npz = np.load(npz_path, allow_pickle=True)
    except Exception as e:
        raise RuntimeError(f"Error loading npz file {npz_path}: {e}")
    prob = npz[npz.files[0]].astype(np.float32)
    out_list = []
    for i in range(0, prob.shape[0]):
        out = np.swapaxes(prob[i], 0, 2)
        n_nan = np.count_nonzero(np.isnan(out))
        if n_nan > 0:
            print(f"NaN values found in {npz_path}: {n_nan}")
        out_list.append(out)
        if save_nifti:
            if not nifti_dir.exists():
                nifti_dir.mkdir(parents=True)
            nib.save(
                nib.Nifti1Image(out.astype(np.float32), affine=np.eye(4)), 
                nifti_dir / f"{npz_path.name.split('.npz')[0]}_{i}_{suffix}.nii.gz"
            )
    
    return np.stack(out_list, axis=0).astype(np.float32)

def get_ensemble(
    nnunet_npz_path_list,
    nnunet_resenc_npz_path_list,
    mednext_npz_path_list,
    mednext_pkl_path_list,
    ensembled_path, 
    input_img,
    weights=[1.0, 1.0, 1.0]
):
    if not ensembled_path.exists():
        ensembled_path.mkdir(parents=True)
        
    case = nnunet_npz_path_list[0].name.split('.npz')[0]
    print(f"Ensemble {case}")
        
    # if os.path.exists(ensembled_path / f"{case}.nii.gz"):
    #     return ensembled_path / f"{case}.nii.gz"

    # nnunet
    prob_nnunet = convert_npz_nnunet(nnunet_npz_path_list[0])
    for i in range(1, len(nnunet_npz_path_list)):
        prob_nnunet += convert_npz_nnunet(nnunet_npz_path_list[i])
    prob_nnunet /= len(nnunet_npz_path_list)
    print(f"Probabilities nnUNet: {prob_nnunet.shape} {prob_nnunet.dtype} {prob_nnunet.min()} {prob_nnunet.max()}")
    # nnunet_resenc
    prob_nnunet_resenc = convert_npz_nnunet(nnunet_resenc_npz_path_list[0])
    for i in range(1, len(nnunet_resenc_npz_path_list)):
        prob_nnunet_resenc += convert_npz_nnunet(nnunet_resenc_npz_path_list[i])
    prob_nnunet_resenc /= len(nnunet_resenc_npz_path_list)
    print(f"Probabilities nnUNet ResEnc: {prob_nnunet_resenc.shape} {prob_nnunet_resenc.dtype} {prob_nnunet_resenc.min()} {prob_nnunet_resenc.max()}")
    # mednext
    prob_mednext = convert_npz_mednext(mednext_npz_path_list[0], mednext_pkl_path_list[0])
    for i in range(1, len(mednext_npz_path_list)):
        prob_mednext += convert_npz_mednext(mednext_npz_path_list[i], mednext_pkl_path_list[i])
    prob_mednext /= len(mednext_npz_path_list)
    print(f"Probabilities MedNeXt: {prob_mednext.shape} {prob_mednext.dtype} {prob_mednext.min()} {prob_mednext.max()}")
    
    final_prob = weights[0] * prob_nnunet + weights[1] * prob_nnunet_resenc + weights[2] * prob_mednext
    final_prob /= sum(weights)
    print(f"Final probabilities: {final_prob.shape} {final_prob.dtype} {final_prob.min()} {final_prob.max()}")

    seg = np.argmax(final_prob, axis=0)
    print(f"Seg: {seg.shape} {seg.dtype} {seg.min()} {seg.max()}")
    # save seg
    img = nib.load(input_img)
    nib.save(nib.Nifti1Image(seg.astype(np.int8), img.affine), ensembled_path / f"{case}.nii.gz")
    return ensembled_path / f"{case}.nii.gz"
