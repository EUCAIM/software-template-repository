import os

import numpy as np
import nibabel as nib
from pyrobex.robex import robex
from scipy.ndimage import label

def apply_default_mask(task:str, t1_path:str, output_path:str):
    """
    Apply a default mask to the given T1-weighted MRI image.

    Parameters:
    - task (str): The task name, e.g., 't1'.
    - t1_path (str): Path to the input T1-weighted MRI image.
    - output_path (str): Path to save the masked output image.

    Returns:
    - None
    """

    template_path = f"/mlcube_project/default_mask/heatmap_GLI_best_threshold_fold.nii.gz"

    t1_image = nib.load(t1_path)
    if task in ['PED', 'MEN-RT']:
        _, brainmask = robex(t1_image)
    else:
        brainmask = t1_image
    brainmask = brainmask.get_fdata() > 0
    # template_path_exists then load the template
    
    if os.path.exists(template_path):
        print(f"Using template mask from {template_path}")
        template_img = nib.load(template_path)
        template_data = template_img.get_fdata()
        # get the unique value of the template to use as mask
        unique_vals = np.unique(template_data)[-1]
        template_data = template_data * (brainmask)
        # keep only the largest connected component
        labeled_array, num_features = label(template_data)
        if num_features > 0:
            counts = np.bincount(labeled_array.flat)
            counts[0] = 0  # background is label 0
            largest_label = counts.argmax()
            template_data = (labeled_array == largest_label).astype(np.uint8) * unique_vals
    else:
        template_data = brainmask # fallback to brainmask for MET and MENRT
        if task == 'MET':
            template_data = template_data * 3
    
    # save the mask using t1 header and affine
    mask_img = nib.Nifti1Image((template_data).astype(np.uint8),  t1_image.affine, t1_image.header)
    nib.save(mask_img, output_path)
    print(f"Saved default masked image to {output_path}")
import os

import numpy as np
import nibabel as nib
from pyrobex.robex import robex
from scipy.ndimage import label

def apply_default_mask(task:str, t1_path:str, output_path:str):
    """
    Apply a default mask to the given T1-weighted MRI image.

    Parameters:
    - task (str): The task name, e.g., 't1'.
    - t1_path (str): Path to the input T1-weighted MRI image.
    - output_path (str): Path to save the masked output image.

    Returns:
    - None
    """

    t1_image = nib.load(t1_path)
    if task in ['PED', 'MEN-RT']:
        _, brainmask = robex(t1_image)
    else:
        brainmask = t1_image
    template_data = brainmask.get_fdata() > 0

    labeled_array, num_features = label(template_data)
    if num_features > 0:
        counts = np.bincount(labeled_array.flat)
        counts[0] = 0  # background is label 0
        largest_label = counts.argmax()
        template_data = (labeled_array == largest_label).astype(np.uint8)
    if task == 'GLI':
        template_data = template_data * 3
    elif task == 'PED':
        template_data = template_data * 2
    elif task == 'MEN-RT':
        template_data = template_data * 1
    elif task == 'MET':
        template_data = template_data * 0
        
    
    # save the mask using t1 header and affine
    mask_img = nib.Nifti1Image((template_data).astype(np.uint8),  t1_image.affine, t1_image.header)
    nib.save(mask_img, output_path)
    print(f"Saved default masked image to {output_path}")
