# Bug Localization by Using Bug Reports (DNN+rVSM)

- This study and implementation is adapted from the study [*Bug Localization with Combination of Deep Learning and Information Retrieval*](https://ieeexplore.ieee.org/document/7961519).


## Dataset

- For our implementation, the dataset of *Denchmark* is used.
	- The dataset of source files is created from the [original repository (Denchmark)](https://github.com/RosePasta/Denchmark_BRs).
	- The bug dataset can be accessed from [here](https://github.com/RosePasta/Denchmark_BRs).


## Approach
- Before implementing this model, convert the json files from Denchmark dataset (or any other dataset) to CSV file (Use the code "data_preprocess_JSON_to_CSV.ipynb" for converting)

- Then run the "data_preprocess_CSV_to_TSV_for_DNN+rVSM.ipynb" to process the CSV files for the model

- In previous studies, a cosine similartiy based information retrieval model ,rVSM, has been used and resulted with good top-k accuracy results. In our case, rVSM approach is combined with some other metadata and fed to a deep neural network to conclude withg a relevancy score between a bug report and a source code file. This final relevany scores between all bug reports and source files are kept and top-k accuracy results for k=1,5,10,20 are calculated. In the original study, top-20 accuracy is found to be about 85% where our implementation achieves a _____ top-20 accuracy.
