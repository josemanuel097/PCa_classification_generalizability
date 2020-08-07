# PCa_classification_generalizability


## Introduction 

This repository contains the code used to test the generalizability of radiomics model in the context of prostate cancer classification. For this experiment we used the open source python package named Worflow for Optimal Radiomics Classification. The detail about how to use this software can be found in WORC's documentation.  We would like to invite researchers working with data sets formed by multiple healtcare centers and scanner to try this code with their own data, and comment their results. To make easier the understanding of how to use this code, this repository includes a functional demostration on PROSTATEX data set. 

Disclaimer: The data inside this repository is limited and is meant to be used only as example to learn how to adapt yuour data to this experiment. The results obtained with this limited set should not be considered for analyisis or making conclusions.

## Example Tutorial: Data organization.

### Image_data:

To make this code work with your data, the MR images should have the following structure. 

Patient_folder_from_center_A/Patient#/MR_sequence/Patient#__.nii

                                                
### Labels: 
The labels for the patient should included in a txt file following this format. 

Patient    Label

Patient1   1
Patient2   0


## Requirements.

Package requirements can be found in requirements.txt


