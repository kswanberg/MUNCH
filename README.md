# MUNCH: Masking Under Needless Contrast Helper

MUNCH (Masking Under Needless Contrast Helper) automatically detects moderately sized contiguous 2D signals starting from the edges of images and replaces their offending rows and columns with background noise. The original use case for  MUNCH was removing nearby brain slices from 2-channel confocal microscopy images targeting a single center slice, but this tool can be employed out-of-box for any two-channel TIFF files for which unwanted 2D signals appear from the edges, as well as further adapted to a wider range of applications.  


### Inputs

Upon function run the user will be prompted to select an input directory expected to contain two-channel TIFF files to be munched. 


### Outputs

MUNCH outputs into the working directory (typically the folder in which the script lives unless otherwise defined) a directory with the prefix "MUNCH_Outputs_" and a suffix based on the date-time, and which contains the following contents, wherein 'X' is the name of the input image: 

* Difference images between the first channel of the original input TIFFs and the first channel of the munched outputs. These are labeled '00_diff_mnched_X.tif'. 

* Munched outputs as unsplit two-channel TIFFs. These are labeled '01_mnched_nosplt_X.tif'. 

* Munched outputs as individual channels of split two-channel TIFFs. These are labeled '02a_mnched_splt_ch0_X.tif' and '02b_mnched_splt_ch1_X.tif' for the first and second image channels, respectively. Note that these output pairs can be used as input images for related program BIICHT: Batch Image Intensity Calculation Helper Tool. 


### Citation 

Work that employed code from MUNCH can cite it as follows: 

Swanberg, K.M. (2024). MUNCH: Masking Under Needless Contrast Helper v. 1.1. Source code. https://github.com/kswanberg/MUNCH.


### Developer

Please send comments and questions to [Kelley Swanberg](mailto:kelley.swanberg@med.lu.se). 