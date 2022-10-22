#This file calls all different classes for product to function

#Setup Pseudocode (will be removed later)

# intiitalize variables

#Open Access to Webcam and run (forever)
# System is running forever:
#   LOOP CONDITION: vaiables = sample_count, sample_time, max_samples
#       sample_current_count must be less than = max_samples
#       sample_count < (max_samples) aka 60 (60 samples per second)
#       sample_time < (max_sample_time) aka 30 seconds 
#   
#   
#   if time%sample_time == 0:
#       1. preprocess_image() (Input: Image File, Output: Image File)
#       2. run_model() (Input: Image File, Output: BoundaryBoxes+Classifications+ConfidenceScores)
#       3. store_output() (Input: Model Output, Output: NULL - stores data in local folder(samples))
#       4. (sample_current_count++)
#       5. Logging Info??? (Time, Raw_Image,Preprocessed,Model_Output)
# 
#       If (batched_samples):
#          1. if (sample_current_count) = (sample_count) then:
#               a. combine_samples() = (Input: Folder with Image Data, Output: Single Image Output)
#               b. to_webapp() = (Input: Folder with samples, Output: NULL - sends to webapp)
#               c. (sample_current_count) = 0
#               d. Logging Info??? (Time, Single Image Output)
#       Else:
#           1. to_webapp() = (Input: Folder with samples, Output: NULL - sends to webapp)
#           2. sample_current_count = 0
#           3. Logging Info??? (Time, Single Image Output)
#   time++      
#
# Error messages will be needed for each inner function
# Testing function for the system loop in case it fails -> will only run during testing, turned off when running for data processing
#       Conditions: vaiables = sample_count, sample_time, max_samples
# Other functions to conisder: using time to check model tun time, preprocessing and postprocessing time, also webapp time
# for testing webapp -> maybe have it send a message back?

# Other things: how exactly to log, what data to log
