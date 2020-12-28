#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 11:34:58 2019

@author: jose
"""
#Import the packages for this experiment

import WORC
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
import sys
import glob



requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# The inputs in work must be defined as dictionaries with a single 
# identifier per patient(key) and the path to the image location(value).Furthermore, 
# a dictionary per image sequence (lesion segmentation ,T2,DWI and ADC in our case)
# must be generated. This function in particular takes as input the path to the data
# from one specific center and returns all the patients dictionaries with the
# paths to their segmentations and sequences.
 

def create_sources(datapath):
    


    if isinstance(datapath,list):#To combine 2 datasets for the test set.
        patient_folders = []
        for fol in datapath:  
            patients = glob.glob(fol + '/*')
            patient_folders.append(patients)
        
        patient_folders = patient_folders[0] + patient_folders[1] 
    
    else:
        patient_folders= glob.glob(datapath + '/*')       
    
    #Create sequences dictionaries
    segmentations = dict()
    images_adc = dict()
    images_t2 = dict()
    images_dwi = dict()
    
    #define sequences paths per patient and save in the dictionaries.
    for p in patient_folders:
        laesion_files = glob.glob(p + '/*_ADC.nii.gz')
        if len(laesion_files) == 1:
            # Single lesion for patient
            PID = os.path.basename(laesion_files[0])[:-11]

            segmentations[PID] = glob.glob(p + '/*_mask.nii.gz')[0]
            images_adc[PID]    = glob.glob(p + '/*_ADC.nii.gz')[0]
            images_dwi[PID]    = glob.glob(p + '/*_DWI.nii.gz')[0]
            images_t2[PID]     = glob.glob(p + '/*_T.nii.gz')[0]
        else:
            # multiple laesions
            for lf in laesion_files:
                PID = os.path.basename(lf)[:-4]
                
                segmentations[PID] = glob.glob(p + '/*_mask.nii.gz')[0]
                images_adc[PID]    = glob.glob(p + '/*_ADC.nii.gz')[0]
                images_dwi[PID]    = glob.glob(p + '/*_DWI.nii.gz')[0]
                images_t2[PID]     = glob.glob(p + '/*_T.nii.gz')[0]

    return segmentations, images_t2, images_dwi, images_adc

# To define WORC configuration without/without combat , and 10000 iterations.
# During feature selection, group of features could be used or neglected.

def editconfig(config):
    
    
    config['General']['Segmentix'] = 'False'
    config['General']['ComBat'] = 'False'   
    
    
    config['ComBat']['mod'] = '[]'
    config['ComBat']['batch'] = 'Hospital'

    
    config['General']['FeatureCalculators'] = '[predict/CalcFeatures:1.0]'   
    config['General']['tempsave'] = 'True'
    config['SelectFeatGroup']['shape_features'] = 'True, False'
    config['SelectFeatGroup']['histogram_features'] = 'True, False'
    config['SelectFeatGroup']['orientation_features'] = 'True, False'
    config['SelectFeatGroup']['patient_features'] = 'False'
    config['SelectFeatGroup']['semantic_features'] = 'False'
    config['SelectFeatGroup']['coliage_features'] = 'False'
    config['SelectFeatGroup']['vessel_features'] = 'True, False'
    config['SelectFeatGroup']['phase_features'] = 'True, False'
    config['SelectFeatGroup']['log_features'] = 'True, False'

    config['ImageFeatures']['coliage'] = 'False'
    config['ImageFeatures']['vessel'] = 'True'
    config['ImageFeatures']['phase'] = 'True'
    config['ImageFeatures']['log'] = 'True'

    config['ImageFeatures']['image_type'] = 'MR'
    config['Classification']['fastr'] = 'True'

    config['CrossValidation']['N_iterations'] = '100'
    config['HyperOptimization']['N_iterations'] = '10000'
    config['HyperOptimization']['n_jobspercore'] = '200'
    config['Featsel']['Variance'] = '1.0'
    config['Featsel']['UsePCA'] = '0.25'


    config['Labels']['label_names'] = 'Label'
    config['Labels']['modus'] = 'singlelabel'
    config['SampleProcessing']['SMOTE'] = 'True'
    config['SampleProcessing']['Oversampling'] = 'True'
 

   # In feature selection, just use all features
    config['SelectFeatGroup']['toolbox'] = 'All,PREDICT,PyRadiomics'    


    config['Classification']['fastr_plugin'] = 'DRMAAExecution'
    return config


def selectsources(option, settings, name):
    # Change this for your personal settings
    filedir = os.path.dirname(os.path.realpath(__file__))
    location = 'Cluster'
    network = WORC.WORC(name)

    # NOTE: Make sure these files are in your input mount
    # We add labels either for training and test set
    network.labels_train.append("vfs://home/worc_prostate/Labels_hospital.txt")
    network.labels_test.append("vfs://home/worc_prostate/Labels_hospital.txt")
    # network.semantics_train.append("vfs://home/worc_prostate/sem_Prostate.csv")


   #Define the path for train and test data.
    path ='/home/jtovar/PCa_classification_generalizability/Data_sets_example/Set_A'
    path_test =['/home/jtovar/PCa_classification_generalizability/Data_sets_example/Set_B',
                '/home/jtovar/PCa_classification_generalizability/Data_sets_example/Set_C']
    



    segmentations, images_t2, images_dwi, images_adc =\
          create_sources(path)
          
   
   #Append data dictionaries to train set, eacth time we add a sequence
   # a segmentation path must be indicated. In our case we used the same 
   # segmentation given that out data was registered.
   
    network.images_train.append(images_t2)
    network.segmentations_train.append(segmentations)
    print(images_t2)
    network.images_train.append(images_dwi)
    network.segmentations_train.append(segmentations)

    network.images_train.append(images_adc)
    network.segmentations_train.append(segmentations)


   #Append data dictionaries for the test set 
    segmentations_t, images_t2_t, images_dwi_t, images_adc_t =\
       create_sources(path_test)            

   
    network.images_test.append(images_t2_t)
    network.segmentations_test.append(segmentations_t)
    print(images_t2_t)
    network.images_test.append(images_dwi_t)
    network.segmentations_test.append(segmentations_t)

    network.images_test.append(images_adc_t)
    network.segmentations_test.append(segmentations_t)            
   

    config = network.defaultconfig()
    config['Labels']['label_names'] = 'Label'
    config = editconfig(config)

   # We have three images per patient, hence three configs
    network.configs.append(config)
    network.configs.append(config)
    network.configs.append(config)
            
            
            


    network.build()
    network.add_evaluation('Label')    
    network.set()
    return location, network


def main(options, names):
    # NOTE:Change this for your personal settings
    tempdir_cluster = '/scratch/jtovar/tmp/'

    settings = dict()

    # NOTE:Do you have the files locally?
    source = 'local'
    if source == 'xnat':
        settings['File'] = 'xnat'
    else:
        settings['File'] = 'local'

    # Use ring segmentation or normal?
    settings['Seg'] = 'Normal'

    for option, name in zip(options, names):
        location, network = selectsources(option, settings, name)
        tempdir = os.path.join(tempdir_cluster, name)

        network.fastr_tempdir = tempdir
        network.fastr_plugin = 'DRMAAExecution'
        network.execute()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        options = ['Label']
        names = ['train_a_test_ab_classi']
    elif len(sys.argv) != 3:
        raise IOError("This function accepts two arguments")
    else:
        options = [str(sys.argv[1])]
        names = [str(sys.argv[2])]
    main(options, names)
