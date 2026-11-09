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
    if task == 'MEN':
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
