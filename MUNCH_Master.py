import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename 
from matplotlib import image as img
from matplotlib import pyplot as plt
from skimage import io
import numpy as np
import cv2
import os
import datetime
import pandas as pd
from scipy.ndimage import gaussian_filter
import logging 
import sys 
from skimage import io
from tifffile import imwrite
import copy 
from skimage import data
from skimage.filters import threshold_otsu

def MUNCH_Master(): 

    # Courtesy of https://patorjk.com/software/taag/#p=testall&f=Graffiti&t=MUNCH
    print("""\n\n\n         
              
                ███╗   ███╗██╗   ██╗███╗   ██╗ ██████╗██╗  ██╗
                ████╗ ████║██║   ██║████╗  ██║██╔════╝██║  ██║
                ██╔████╔██║██║   ██║██╔██╗ ██║██║     ███████║
                ██║╚██╔╝██║██║   ██║██║╚██╗██║██║     ██╔══██║
                ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║╚██████╗██║  ██║
                ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝ Masking Under Needless Contrast Helper \n""")

     # Provide initial instructions to the new user 
    print("""
           Welcome to MUNCH (pronounced "MON-ke"), your solution for batch microscopy image cropping! This tool finds unwanted large tissue fragments on the edges of your images
           and replaces them with randomized background pixels. Note that this tool is not designed to work on images in which tissue fragments are large enough to encroach on the 2D coordinates
           values of your central microscopy targets. \n""") 
    print('Please select the directory of images to be munched! Images are currently expected to be 2-channel TIFFs. \n') 

    # Set working directory to location of file 
    os.chdir(sys.path[0])

    # Create output directory 
    time_for_dirname = datetime.datetime.now() 
    root_dirname = str('MUNCH_Outputs_' + str(time_for_dirname)).replace(' ', '_')
    root_dirname = root_dirname.replace(':', '')
    root_dirname = root_dirname.replace('.', '')
    os.mkdir(root_dirname)

    # Create error log
    log_name = str(root_dirname + '\\' 'MUNCH_log.txt')
    logging.basicConfig(filename=log_name, level=logging.INFO)

    # Adapted from https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog
    Tk().withdraw()
    FilePathtoInputs = askopenfilename()
    print(FilePathtoInputs)

    image_directory = os.path.dirname(FilePathtoInputs);
    directory_inputs = os.listdir(image_directory); 
    num_files = np.shape(directory_inputs)[0]; 

    zero_image_margin_coeff = 0.10; 
    munch_margin_coeff = 0.015; 
    threshold_coeff = 0.6; 

    for kk in range(num_files): 

        kk_name = directory_inputs[kk]; 
        image_to_eat = '%s/%s' % (image_directory, kk_name); 
        image_to_eat_filename = os.path.basename(image_to_eat); 
        image_to_eat_filename_noext =  os.path.splitext(image_to_eat_filename); 

        image_pre_munch = cv2.imread(image_to_eat); 

        image_pre_munch_dim = np.shape(image_pre_munch); 

        munchcounter = 0; 
        highest_munchcounter = 0;
        last_munchcounter = 0; 
        current = 0;  
        comparator = 0; 

        left_crop_found = 0; 
        right_crop_found = 0;
        top_crop_found = 0; 
        bottom_crop_found = 0; 

        left_crop = 0; 
        right_crop = 0;
        top_crop = 0; 
        bottom_crop = 0; 

        left_munchcounter_threshold = round(zero_image_margin_coeff*image_pre_munch_dim[0]); 
        right_munchcounter_threshold = round(zero_image_margin_coeff*image_pre_munch_dim[0]); 
        top_munchcounter_threshold = round(zero_image_margin_coeff*image_pre_munch_dim[1]); 
        bottom_munchcounter_threshold = round(zero_image_margin_coeff*image_pre_munch_dim[1]); 

        left_right_munch_margin = round(munch_margin_coeff*image_pre_munch_dim[1]); 
        top_bottom_munch_margin = round(munch_margin_coeff*image_pre_munch_dim[0]); 

        # Walk through image columns from the left 
        for ii in range(10, image_pre_munch_dim[1], 1):

            if left_crop_found !=1: 
                
                # Walk down each column from the top
                for jj in range(image_pre_munch_dim[0]):

                    current = copy.deepcopy(image_pre_munch[jj, ii, 0]);
                
                    if munchcounter > highest_munchcounter:
                        highest_munchcounter = copy.deepcopy(munchcounter);
                    
                    if current > 2: 
                        if munchcounter == 0 and comparator < 3:
                            comparator = copy.deepcopy(current); 
                            munchcounter = 1; 
                        else: 
                            if comparator > 2:
                                comparator = copy.deepcopy(current); 
                                munchcounter = munchcounter + 1;
                    else:
                        munchcounter = 0; 
                        comparator = 0; 
            
                last_munchcounter = copy.deepcopy(highest_munchcounter); 
                comparator = 0; 
                current = 0; 
                munchcounter = 0;  

                if highest_munchcounter < left_munchcounter_threshold:
                    if last_munchcounter < left_munchcounter_threshold:
                        left_crop_found = 1; 
                        if ii > 1:
                            left_crop = ii; 
                    else: 
                        left_crop = 0; 
        
                highest_munchcounter = 0;

        if left_crop == 10: 
            left_crop = 0; 
        else:
            left_crop = left_crop + left_right_munch_margin; 
                        
        print('Left crop is: ', left_crop); 

        munchcounter = 0; 
        highest_munchcounter = 0;
        last_munchcounter = 0; 
        current = 0;  
        comparator = 0; 

        # Walk through image columns from the right
        for ii in range(image_pre_munch_dim[1]-11, 0, -1):

            if right_crop_found !=1: 
                # Start from the top
                for jj in range(image_pre_munch_dim[0]):

                    current = copy.deepcopy(image_pre_munch[jj, ii, 0]);
                
                    if munchcounter > highest_munchcounter:
                        highest_munchcounter = copy.deepcopy(munchcounter);
                    
                    if current > 2: 
                        if munchcounter == 0 and comparator < 3:
                            comparator = copy.deepcopy(current); 
                            munchcounter = 1; 
                        else: 
                            if comparator > 2:
                                comparator = copy.deepcopy(current); 
                                munchcounter = munchcounter + 1;
                    else:
                        munchcounter = 0; 
                        comparator = 0; 
            
                last_munchcounter = copy.deepcopy(highest_munchcounter); 
                comparator = 0; 
                current = 0; 
                munchcounter = 0;   

                if highest_munchcounter < right_munchcounter_threshold:
                    if last_munchcounter < right_munchcounter_threshold:
                        right_crop_found = 1; 
                        if ii > 1:
                            right_crop = ii; 
                    else: 
                        right_crop = image_pre_munch_dim[1]; 
                    
                highest_munchcounter = 0;

        if right_crop == image_pre_munch_dim[1]-11: 
            right_crop = image_pre_munch_dim[1];
        else:
            right_crop = right_crop - left_right_munch_margin;  
                        
        print('Right crop is: ', right_crop); 

        munchcounter = 0; 
        highest_munchcounter = 0;
        last_munchcounter = 0; 
        current = 0;  
        comparator = 0; 

        # Walk through image rows from the top 
        for ii in range(10, image_pre_munch_dim[0], 1):
            
            if top_crop_found !=1: 
                # Start from the left
                for jj in range(image_pre_munch_dim[1]):

                    current = copy.deepcopy(image_pre_munch[ii, jj, 0]);
                
                    if munchcounter > highest_munchcounter:
                        highest_munchcounter = copy.deepcopy(munchcounter);
                    
                    if current > 2: 
                        if munchcounter == 0 and comparator < 3:
                            comparator = copy.deepcopy(current); 
                            munchcounter = 1; 
                        else: 
                            if comparator > 2:
                                comparator = copy.deepcopy(current); 
                                munchcounter = munchcounter + 1;
                    else:
                        munchcounter = 0; 
                        comparator = 0; 
            
                last_munchcounter = copy.deepcopy(highest_munchcounter); 
                comparator = 0; 
                current = 0; 
                munchcounter = 0;  

                if highest_munchcounter < top_munchcounter_threshold:
                    if last_munchcounter < top_munchcounter_threshold:
                        top_crop_found = 1; 
                        if ii > 1:
                            top_crop = ii; 
                    else: 
                        top_crop = 0; 

                highest_munchcounter = 0;

        if top_crop == 10: 
            top_crop = 0; 
        else:
            top_crop = top_crop + top_bottom_munch_margin;  

        print('Top crop is: ', top_crop); 

        munchcounter = 0; 
        highest_munchcounter = 0;
        last_munchcounter = 0; 
        current = 0;  
        comparator = 0; 

        # Walk through image rows from the bottom 
        for ii in range(image_pre_munch_dim[0]-11, 0, -1):

            if bottom_crop_found !=1: 
                # Start from the left
                for jj in range(image_pre_munch_dim[1]):

                    current = copy.deepcopy(image_pre_munch[ii, jj, 0]);
                
                    if munchcounter > highest_munchcounter:
                        highest_munchcounter = copy.deepcopy(munchcounter);
                    
                    if current > 2: 
                        if munchcounter == 0 and comparator < 3:
                            comparator = copy.deepcopy(current); 
                            munchcounter = 1; 
                        else: 
                            if comparator > 2:
                                comparator = copy.deepcopy(current); 
                                munchcounter = munchcounter + 1;
                    else:
                        munchcounter = 0; 
                        comparator = 0; 
            
                last_munchcounter = copy.deepcopy(highest_munchcounter); 
                comparator = 0; 
                current = 0; 
                munchcounter = 0; 

                if highest_munchcounter < bottom_munchcounter_threshold:
                    if last_munchcounter < bottom_munchcounter_threshold:
                        bottom_crop_found = 1; 
                        if ii > 1:
                            bottom_crop = ii; 
                    else: 
                            bottom_crop = image_pre_munch_dim[0];   

                highest_munchcounter = 0;  

        if bottom_crop == image_pre_munch_dim[0]-11: 
            bottom_crop = image_pre_munch_dim[0]; 
        else:
            bottom_crop = bottom_crop - top_bottom_munch_margin;  

        print('Bottom crop is: ', bottom_crop); 

        # Reload the data with both channels 
        image_pre_munch_multich = io.imread(image_to_eat); 
        image_munched_multich_new = copy.deepcopy(image_pre_munch_multich); 

        # Find the best threshold for differentiating signal from noise
        thresh_multich_1 = threshold_coeff*threshold_otsu(image_pre_munch_multich[0, :, :]); # Extra-conservative
        thresh_multich_2 = threshold_coeff*threshold_otsu(image_pre_munch_multich[1, :, :]); # Extra-conservative
        background_val_1 = np.min(image_pre_munch_multich[0, :, :][np.nonzero(image_pre_munch_multich[0, :, :])]);  
        background_val_2 = np.min(image_pre_munch_multich[1, :, :][np.nonzero(image_pre_munch_multich[1, :, :])]); 

        # Now munch to the crop points!
        replacement_line_left = copy.deepcopy(image_pre_munch_multich[:, :, left_crop + 11]); 
        replacement_line_left[0][replacement_line_left[0]>thresh_multich_1] = background_val_1; 
        replacement_line_left[1][replacement_line_left[1]>thresh_multich_2] = background_val_2;

        replacement_line_right = copy.deepcopy(image_pre_munch_multich[:, :, right_crop - 11]); 
        replacement_line_right[0][replacement_line_right[0]>thresh_multich_1] = background_val_1; 
        replacement_line_right[1][replacement_line_right[1]>thresh_multich_2] = background_val_2; 

        replacement_line_top = copy.deepcopy(image_pre_munch_multich[:, top_crop + 11, :]); 
        replacement_line_top[0][replacement_line_top[0]>thresh_multich_1] = background_val_1; 
        replacement_line_top[1][replacement_line_top[1]>thresh_multich_2] = background_val_2;

        replacement_line_bottom = copy.deepcopy(image_pre_munch_multich[:, bottom_crop - 11, :]); 
        replacement_line_bottom[0][replacement_line_bottom[0]>thresh_multich_1] = background_val_1; 
        replacement_line_bottom[1][replacement_line_bottom[1]>thresh_multich_2] = background_val_2;

        # Munch to the left crop point
        for ii in range(left_crop):
            replacement_line_left_new = copy.deepcopy(replacement_line_left); 
            np.transpose(np.random.shuffle(np.transpose(replacement_line_left_new)));
            image_munched_multich_new[:, :, ii] = replacement_line_left_new; 

        # Munch to the right crop point
        for ii in range(image_pre_munch_dim[1]-1, right_crop, -1):
            replacement_line_right_new = copy.deepcopy(replacement_line_right); 
            np.transpose(np.random.shuffle(np.transpose(replacement_line_right_new)));
            image_munched_multich_new[:, :, ii] = replacement_line_right_new; 

        # Munch to the top crop point
        for ii in range(top_crop):
            replacement_line_top_new = copy.deepcopy(replacement_line_top); 
            np.transpose(np.random.shuffle(np.transpose(replacement_line_top_new)));
            image_munched_multich_new[:, ii, :] = replacement_line_top_new; 

        # Munch to the bottom crop point
        for ii in range(image_pre_munch_dim[0]-1, bottom_crop, -1):
            replacement_line_bottom_new = copy.deepcopy(replacement_line_bottom); 
            np.transpose(np.random.shuffle(np.transpose(replacement_line_bottom_new)));
            image_munched_multich_new[:, ii, :] = replacement_line_bottom_new; 

        image_munched_difference = image_munched_multich_new[0, :, :] - image_pre_munch_multich[0, :, :]; 

        image_munched_difference_filename = '%s/00_diff_mnchd_%s.tif' % (root_dirname, image_to_eat_filename_noext[0]); 
        image_munched_nosplit_filename = '%s/01_mnchd_nosplt_%s.tif' % (root_dirname, image_to_eat_filename_noext[0]); 
        image_munched_split_ch0_filename = '%s/02a_mnchd_splt_ch0_%s.tif' % (root_dirname, image_to_eat_filename_noext[0]); 
        image_munched_split_ch1_filename = '%s/02b_mnchd_splt_ch1_%s.tif' % (root_dirname, image_to_eat_filename_noext[0]); 

        imwrite(image_munched_difference_filename, image_munched_difference, imagej=True); 
        imwrite(image_munched_nosplit_filename, image_munched_multich_new, imagej=True);  
        imwrite(image_munched_split_ch0_filename, image_munched_multich_new[0, :, :], imagej=True); 
        imwrite(image_munched_split_ch1_filename, image_munched_multich_new[1, :, :], imagej=True); 

MUNCH_Master(); 