# Experimental results
This folder consists of python files for answering first research questions.

## Steps
1. Setting the absolute path in _z_config.txt_
    - Just copy and paste a set of paths from the 1_dataset_generation folder z_config.
2. Execute each file for all three methodologies.

a) **a_buglocator_bluir_rq1_data.py** & b)**b_buglocator_bluir_rq1_result.py** : Evaluate the BugLocator and BLUiR model using Top@K ranking, MRR & MAP. Generates the result on results.rq1.txt and has been converted results_rq1_buglocator_bluir.csv

c) **c_BLIA_data.py** & d) **d_BLIA_result.py** : Evaluate the BLIA model using Top@K ranking, MRR & MAP. Generates the result into results_rq3.txt, which is not uploaded here as the text file is 700+ mb. (Here the results_rq3.txt has been converted to csv as results_rq1_BLIA.csv)
