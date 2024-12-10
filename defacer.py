from __future__ import generators

import glob
import os
import functools
import sys
import argparse
import nibabel as nib
import SimpleITK as sitk
import numpy as np
from scipy import ndimage
import logging
# Ensure HDBET is in the Python path
sys.path.append('../')
sys.path.append("./HDBET/")

from HDBET.HD_BET.run import run_hd_bet  # Ensure you've cloned the HDBET repo

def dilate_mask(mask_data, dilation_radius=2, connectivity=1):
    """
    Dilate a 3D binary mask using SciPy's ndimage module.

    Parameters:
    - input_mask_path (str): Path to the input NIfTI mask.
    - output_mask_path (str): Path where the dilated mask will be saved.
    - dilation_radius (int): Radius for dilation (number of iterations).
    - connectivity (int): Structuring element connectivity (1 for 6-connectivity in 3D).
    """
    binary_mask = (mask_data > 0).astype(np.uint8)
    
    struct = ndimage.generate_binary_structure(rank=3, connectivity=connectivity)
    
    dilated_mask = ndimage.binary_dilation(binary_mask, structure=struct, iterations=dilation_radius).astype(np.uint8)
    #print areas of the mask and dilated mask
    print("Mask area: ", np.sum(binary_mask))
    print("Dilated mask area: ", np.sum(dilated_mask))
    return dilated_mask


def create_directory(path):
    """Utility function to create a directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Skull stripping and brain extraction pipeline.")
    parser.add_argument('--CUDA_VISIBLE_DEVICES', type=int, default=0, help='CUDA device ID to use.')
    parser.add_argument('--input_dir', type=str, default='input_nifti', help='Directory containing input NIfTI files.')
    parser.add_argument('--output_path', type=str, default='output', help='Directory to save the final brain-extracted NIfTI files.')
    args = parser.parse_args()

    input_dir = args.input_dir
    output_path = args.output_path
    #check if CUDA_VISIBLE_DEVICES is set to -1, if so, set it to None
    if args.CUDA_VISIBLE_DEVICES == -1:
        cuda_visible_devices = 'cpu'
    else:
        cuda_visible_devices = args.CUDA_VISIBLE_DEVICES

    proj_dir = './'

    # 1. Create a temporary directory for intermediate files
    temp_path = os.path.join(proj_dir, 'temp')
    create_directory(temp_path)

    # Ensure the output directory exists
    create_directory(output_path)
    print(f"Output directory: {output_path}")
    print(f"Temporary directory: {temp_path}")
    
    # Process each NIfTI file in the input directory
    for img_path in glob.glob(os.path.join(input_dir, "*.nii.gz")):
        print(f"Processing: {img_path}")

        # Extract the base filename without extension
        base_filename = os.path.basename(img_path).split(".")[0]

        # Define paths for intermediate files in the temp directory
        skull_stripped_path = os.path.join(temp_path, f"{base_filename}_skull_stripped.nii")
        mask_path = os.path.join(temp_path, f"{base_filename}_skull_strip_mask.nii.gz")

        # 2. Perform skull stripping using HDBET and save intermediate files to temp
        #if cude_visible_devices is None, set it to None
        run_hd_bet(
            img_path,
            skull_stripped_path,
            mode="accurate",
            config_file=os.path.join("HDBET", "HD_BET", "config.py"),
            device=cuda_visible_devices,
            postprocess=False,
            do_tta=True,
            keep_mask=True,
            overwrite=True
        )

        im_mask = nib.load(mask_path).get_fdata()

        # Define the dilation radius
        dilation_radius = 25
        connectivity = 1       # 6-connectivity for 3D
    
        # Perform dilation
        im_mask_dilated=dilate_mask(im_mask, dilation_radius, connectivity)
       
        #read in base image
        base_img = nib.load(img_path)
        base_data = base_img.get_fdata()
        im_brain = base_data * im_mask_dilated

        # Create a new NIfTI image for the brain-extracted data
        brain_img = nib.Nifti1Image(im_brain, affine=base_img.affine)

        # Save the final brain-extracted NIfTI to the output directory
        output_nii_path = os.path.join(output_path, f"{base_filename}_defaced.nii.gz")
        nib.save(brain_img, output_nii_path)

        print(f"Saved brain-extracted image to: {output_nii_path}")
        

if __name__ == "__main__":
    main()