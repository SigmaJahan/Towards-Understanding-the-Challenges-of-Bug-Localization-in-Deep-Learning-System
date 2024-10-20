[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dalhousieuniversity_dalhousie&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dalhousieuniversity_dalhousie) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=dalhousieuniversity_dalhousie&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=dalhousieuniversity_dalhousie) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=dalhousieuniversity_dalhousie&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=dalhousieuniversity_dalhousie) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=dalhousieuniversity_dalhousie&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=dalhousieuniversity_dalhousie) [![Bugs](https://sonarcloud.io/api/project_badges/measure?project=dalhousieuniversity_dalhousie&metric=bugs)](https://sonarcloud.io/summary/new_code?id=dalhousieuniversity_dalhousie) [![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=dalhousieuniversity_dalhousie&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=dalhousieuniversity_dalhousie) [![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=dalhousieuniversity_dalhousie&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=dalhousieuniversity_dalhousie)

# Towards Understanding the Challenges of Bug Localization in Deep Learning Systems
This repository contains the data, experiments, and analysis for the EMSE 2024 submission "Towards Understanding the Challenges of Bug Localization in Deep Learning Systems".

## Abstract
Software bugs cost the global economy billions of dollars annually and claim ~50% of the programming time from software developers. Locating these bugs is crucial but challenging, particularly in deep-learning systems due to their black-box nature. These bugs are also hidden not only in the code but also in the models and training data, which might make traditional debugging methods less effective. In this article, we conduct a large-scale empirical study to better understand the challenges of localizing bugs in deep-learning systems. First, we determine the bug localization performance of five existing techniques using 2,365 bugs from deep-learning systems and 2,913 bugs from traditional systems. We found that existing techniques show significantly poor performance in localizing bugs from deep-learning systems. Second, we evaluate how different bug types in deep learning systems impact bug localization. We found that the effectiveness of localization techniques varied by bug type, highlighting the need for bug-type-specific approaches. For instance, DNNLOC was more effective with model and tensor bugs, while all techniques faced challenges with GPU bugs. Third, we explore the impact of extrinsic bugs on bug localization in deep learning systems. We found that deep learning bugs are often connected to artifacts other than source code (e.g., GPU, training data, external dependencies) and are more prevalent in deep learning systems than in traditional code, contributing to the poor performance of existing localization methods.

## System Requirements
Operating System: Windows 11 or higher <br>
Python Version: 3.9 <br>
Development Environment: VS Code <br>
This experiment has been conducted in 3 parts, with different system configurations
- Dataset Generation
    - RAM: 16GB
    - GPU: N/A
- Scoring
    - RAM: 16GB
    - GPU: N/A
- Experimental Results
    - RAM: 16GB
    - GPU: N/A

## Installation Details

To replicate the work, the following steps should be taken:

### Step 1: Setting Up the Virtual Environment
The first step is to create a virtual environment using the command below:

```python
python -m virtualenv venv
```

### Step 2: Installing Dependencies
After creating the virtual environment, activate the environment by following these [steps](https://docs.python.org/3/library/venv.html) and install the necessary dependencies (23icsme.yaml) by running the following commands:

```python
pip install -r requirements.txt
```
Note: Install Jupyter Notebook Each folder information is provided on readme.md and requirements.txt of each folder. Install python libraries $ pip install -r scripts/requirements.txt (Provided in each folder)

## Dataset
- Download Denchmark-BRs (DLSW)
    - https://github.com/RosePasta/Denchmark_BRs
- Download BugGL-BRs (NDLSW)
    - https://github.com/muvvasandeep/BuGL

## RQ1_IR
```
IR_based_methods_RQ1
│   README.md
│   23icsme.yaml
└───1_dataset_generation
└───2_scoring
└───3_experimental_results
```
These folders consist of Python files/Jupyter Notebook for the tasks below.

### 1_dataset_generation 

1) a_git_download.py: Download DLSW projects based on Denchmark (output: git_path)
2) b_git_tags_extractor.py: Collect project versions based on Tag info. (output: tag_path)
3) c_bug_repository_generator.py: Divide the bug reports by relevant project version (output: bug_path)
4) d_searchspace_generator.py: Set the search space by relevant project version (= divide all files by the relevant project version) (output: searchspace_path)
5) e1_query_generator.py: Generate query based on regular expression (output: query_path) 
6) e2_query_generator_header.py: Generate query based on HTML header (output: query_path)
7) f_file_class_method_variable_comment_generator.py: Index source files, class, method, variable, and comment (output: file_path, class_path, function_path, variable_path, comment_path)
8) g1_gtf_generator.py: Generate ground truth source files (output: gtf_path))
9) g2_gtf_generator_class_method_variable_comment.py: Generate ground truth for class, methods, variable, and comments (output: gtf_path)
10) h_commit_history_generator.py: Generate commit history (output: commit_path)

### 2_scoring

1) a_similarity_models.py: Compute the similarity between bug reports and source files with rVSM (sf_sim)
    - sf_sim with rVSM reference: Where should the bugs be fixed? More accurate information retrieval-based bug localization based on bug reports, ICSE'12
2) b_bug_sim.py: Compute the similarity between a bug report and historical bug reports (br_sim)
    - br_sim reference: Where should the bugs be fixed? More accurate information retrieval-based bug localization based on bug reports, ICSE'12
3) c_code_structure_sim.py: Compute code structure score - method, class, variable, and comment scores individually 
    - BLUiR Reference: Improving Bug Localization using Structured Information Retrieval (ASE 2013)
4) d_results_combination.py: Combines the scores from method, class, variable, and comment and sums them together for each source file.
5) e_final_similarity_bluir.py: Combines similarity score from a_similarity_models.py (sf_sim), similarity score from e_bug_sim.py (br_sim) and similarity score from h_results_combination.py (bm25_final) for the BluiR methodology.
6) f_final_similarity_buglocator.py: Combines the similarity score from a_similarity_models.py (sf_sim) and similarity score from e_bug_sim.py (br_sim) and uses the equation from the paper for BugLocator methodology.
7) g_strace_score.py: Compute similarity between bug report and stack trace
   - BRATracer reference: Boosting bug-report-oriented fault localization with segmentation and stack-trace analysis, ICSME'14
8) h_commit_score_irbl.py: Compute the commit score 
   - BLIA Reference: Improved bug localization based on code change histories and bug reports, IST'17

### 3_experimental results

1. a) a_buglocator_bluir_rq1_data.py & b) b_buglocator_bluir_rq1_result.py: Evaluate the BugLocator and BLUiR model using Top@K (K= 1, 5, 10) ranking, MRR & MAP. 
2. c) c_BLIA_data.py & d) d_BLIA_result.py: Evaluate the BLIA model using Top@K (K= 1, 5, 10) ranking, MRR & MAP.

All the results from both of the datasets can be found as follows: 
1. results_rq1_buglocator_bluir_Denchmark.csv
2. results_rq1_BLIA_Denchmark.csv
3. results_rq1_buglocator_bluir_BugGL.csv
4. results_rq1_BLIA_BugGL.csv

## RQ1_DL
```
DL_based_methods_RQ1
│   
└───bjXnet
└───DNNLOC
```
## DNNLOC
│   README.md
└───1_Data preprocessing
└───2_Src
### 1_Data preprocessing

1. Before implementing the src code, convert the JSON files from Denchmark dataset (or any other dataset) to CSV file (Use the code "data_preprocess_JSON_to_CSV.ipynb" for converting)
2. Run the "data_preprocess_CSV_to_TSV_for_DNN+rVSM.ipynb" to process the CSV files for the model
   
### 2_Src
1. Run the feature extraction file from src (define the paths accordingly)
2. Run all other files including the main

## bjXnet
│   README.md
│   requirements.txt
└───src
    │   data_processing.py    # Preprocess bug reports and source code
    │   graph_encoder.py      # Code Property Graph and GNN encoder
    │   text_encoder.py       # TextCNN for encoding bug reports and source code
    │   attention_layer.py    # Attention mechanism implementation
    │   bjxnet_model.py       # Full bjXnet model architecture
    │   train.py              # Training script
    │   evaluate.py           # Evaluation script
    │   cpg.py                # To automate CPG automation
    │   utils.py              # Utility functions


## Manual_Analysis_RQ2_RQ3

- a -- BugGL_Manual_Analysis.xlsx & Manual_BugGL.csv: Manual Analysis of BugGL dataset
- b -- Denchmark_Manual_Analysis.xlsx & Manual_Denchmark.csv:  Manual Analysis of Denchmark dataset
- c -- Correlation_Extrinsic_DL.ipynb: Correlation between extrinsic bugs and deep learning bugs
- d -- Analysis_RQ2_RQ3.ipynb: This includes analysis from the manual analysis for RQ2 & RQ3


## Licensing Information
This project is licensed under the MIT License, a permissive open-source license that allows others to use, modify, and distribute the project's code with very few restrictions. This license can benefit research by promoting collaboration and encouraging the sharing of ideas and knowledge. With this license, researchers can build on existing code to create new tools, experiments, or projects, and easily adapt and customize the code to suit their specific research needs without worrying about legal implications. The open-source nature of the MIT License can help foster a collaborative research community, leading to faster innovation and progress in their respective fields. Additionally, the license can help increase the visibility and adoption of the project, attracting more researchers to use and contribute to it.

## Acknowledgment & References
During the implementation of our study, we have referred to the following Github repositories:

1. https://github.com/RosePasta/IRBL_for_DLSW
2. https://github.com/exatoa/Bench4BL
3. https://github.com/klausyoum/BLIA
