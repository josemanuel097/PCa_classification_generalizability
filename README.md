# PCa_classification_generalizability


## Introduction 

<p align="justify"> This repository contains the code used to test the generalizability of radiomics model in the context of prostate cancer classification. For this experiment we used the open source python package named Worflow for Optimal Radiomics Classification. The details about WORC packagee can be found in WORC's documentation (https://worc.readthedocs.io/en/latest/).  We would like to invite researchers working with data sets formed by multiple healtcare centers and scanner to try this code with their own data, and comment their results. To make easier the understanding of how to use this code, this repository includes a demostration based on the PROSTATEX data set. 

<p align="justify"> Disclaimer: The data inside this repository is limited and is meant to be used only as example to learn how to adapt yuour data to this experiment. The results obtained with this limited set should not be considered for analyisis or making conclusions.

## Example Tutorial: Data organization.

### Image_data:

To make this code work with your data, the MR images should have the following structure. 

-Patient_folder_from_center_A/Patient#/Patient#_MRsequence1.nii.gz (T2)

-Patient_folder_from_center_A/Patient#/Patient#_MRsequence2.nii.gz (ADC)

-Patient_folder_from_center_A/Patient#/Patient#_MRsequence3.nii.gz (DWI)

-Patient_folder_from_center_A/Patient#/Patient#_mask.nii.gz (segmentation/ROI)
                                                
### Labels: 
The labels for the patient should included in a txt file following this format. In our case we define as 1 a Gleason Score ≥ 7.

Patient    Label  

Patient_1   1 <br />
Patient_2   0 <br />


## Requirements.

Package requirements can be found in requirements.txt


