[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dalhousieuniversity_dalhousie&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dalhousieuniversity_dalhousie) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=dalhousieuniversity_dalhousie&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=dalhousieuniversity_dalhousie) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=dalhousieuniversity_dalhousie&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=dalhousieuniversity_dalhousie) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=dalhousieuniversity_dalhousie&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=dalhousieuniversity_dalhousie) [![Bugs](https://sonarcloud.io/api/project_badges/measure?project=dalhousieuniversity_dalhousie&metric=bugs)](https://sonarcloud.io/summary/new_code?id=dalhousieuniversity_dalhousie) [![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=dalhousieuniversity_dalhousie&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=dalhousieuniversity_dalhousie) [![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=dalhousieuniversity_dalhousie&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=dalhousieuniversity_dalhousie)

# Towards Automated Bug Localization in Deep Learning Software Systems
This repository contains the data, experiments, and analysis for the project "Towards Automated Bug Localization in Deep Learning Software Systems", conducted as a part of directed study, under the guidance of Dr. Masud Rahman.

Git Repository Link: https://github.com/SigmaJahan/Bug-Localization-IR-based-approaches-for-deep-learning-bugs.git

## Abstract:
Software bugs (errors in computer programs) cost the global economy trillions of dollars annually and claim ~50\% of the programming time from software developers. One of the crucial steps toward correcting a bug is pinpointing its location within the software code,  which is a challenging task. The task is even more challenging with deep learning applications due to their black-box nature. Unlike traditional software bugs, the bugs in deep learning applications are hidden not only in the code but also in the models and training data. Thus, despite decades of research, traditional debugging methods might not be adequate for deep learning bugs due to their unique challenges. Given the rapid growth in deep learning applications, an automated approach for detecting deep learning bugs is highly warranted. The proposed research aims to (a) comprehensively assess the feasibility of traditional debugging methods for detecting deep learning bugs, (b) manual analysis of deep learning software bugs, and (c) gain a deeper understanding of the implication of extrinsic and intrinsic bugs. Recent incidents suggest that deep learning bugs could be costly and fatal (e.g., the Uber SUV accident in Arizona and the Tesla autopilot crash). The proposed research might significantly change the status quo. Our work provides important empirical evidence and actionable insights on deep learning bugs to advance academic research for automated software debugging.  

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

## IR_based_methods_RQ1_DLSW
```
IR_based_methods_RQ1_DLSW
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
4) d_searchspace_generator.py: Set the search space by relevant proejct version (= divide the all files by relevant project version) (output: searchspace_path)
5) e1_query_generator.py: Generate query based on regular expression (output: query_path) 
6) e2_query_generator_header.py: Generate query based on HTML header (output: query_path)
7) f_file_class_method_variable_comment_generator.py: Index source files, class, method, variable and comment (output: file_path, class_path, function_path, variable_path, comment_path)
8) g1_gtf_generator.py: Generate ground truth source files (output: gtf_path))
9) g2_gtf_generator_class_method_variable_comment.py: Generate groud truth for class, methods, variable, comments (output: gtf_path)
10) h_commit_history_generator.py: Generate commit history (outout: commit_path)

By following these steps, you will be able to generate and preprocess the dataset.

### 2_scoring

1) a_similarity_models.py: Compute the similarity between bug reports and source files with rVSM (sf_sim)
    - sf_sim with rVSM reference: Where should the bugs be fixed? more accurate information retrieval-based bug localization based on bug reports, ICSE'12
2) b_bug_sim.py: Compute the similarity between a bug report and historical bug reports (br_sim)
    - br_sim reference: Where should the bugs be fixed? more accurate information retrieval-based bug localization based on bug reports, ICSE'12
3) c_code_structure_sim.py: Compute code structure score - method, class, variable, comment scores individually 
    - BLUiR Reference: Improving Bug Localization using Structured Information Retrieval (ASE 2013)
4) d_results_combination.py: Combines the scores from method, class, variable, comment and sum them together for each source file.
5) e_final_similarity_bluir.py: Combines similarity score from a_similarity_models.py (sf_sim), similarity score from e_bug_sim.py (br_sim) and similarity score from h_results_combination.py (bm25_final) for the BluiR methodology.
6) f_final_similarity_buglocator.py: Combines the similarity score from a_similarity_models.py (sf_sim) and similarity score from e_bug_sim.py (br_sim) and use the    equation from the paper for BugLocator methodology.
7) g_strace_score.py: Compute similarity between bug report and stack trace
   - BRATracer reference: Boosting bug-report-oriented fault localization with segmentation and stack-trace analysis, ICSME'14
8) h_commit_score_irbl.py: Compute the commit score 
   - BLIA Reference: Improved bug localization based on code change histories and bug reports, IST'17

### 3_experimental results

a) a_buglocator_bluir_rq1_data.py & b) b_buglocator_bluir_rq1_result.py: Evaluate the BugLocator and BLUiR model using Top@K (K= 1, 5, 10) ranking, MRR & MAP. Generates the result on results_rq1.txt. 

c) c_BLIA_data.py & d) d_BLIA_result.py: Evaluate the BLIA model using Top@K (K= 1, 5, 10) ranking, MRR & MAP. Generates the result into results_rq3.txt

All the results from both of the dataset can be found as: 
1. results_rq1_buglocator_bluir_Denchmark.csv
2. results_rq1_BLIA_Denchmark.csv
3. results_rq1_buglocator_bluir_BugGL.csv
4. results_rq1_BLIA_BugGL.csv

## Analysis of RQ2 & RQ3

### Manual_analysis_all_ICSME.ipynb 

- Manual_analysis_all_ICSME.ipynb: This includes analysis from the manual analysis for RQ2 & RQ3
- BugGL_Manual_Analysis.xlsx: Manual Analysis of BugGL dataset
- Denchmark_Manual_Analysis.xlsx:  Manual Analysis of Denchmark dataset

## Licensing Information
This project is licensed under the MIT License, a permissive open-source license that allows others to use, modify, and distribute the project's code with very few restrictions. This license can benefit research by promoting collaboration and encouraging the sharing of ideas and knowledge. With this license, researchers can build on existing code to create new tools, experiments, or projects, and easily adapt and customize the code to suit their specific research needs without worrying about legal implications. The open-source nature of the MIT License can help foster a collaborative research community, leading to faster innovation and progress in their respective fields. Additionally, the license can help increase the visibility and adoption of the project, attracting more researchers to use and contribute to it.

## Acknowledgment & References
During the implementation of our study, we have referred the following Github repositories:

1. https://github.com/RosePasta/IRBL_for_DLSW
2. https://github.com/exatoa/Bench4BL
3. https://github.com/klausyoum/BLIA

## Contact Information

For any issues or concerns regarding the replication package, please reach out to Sigma Jahan (sigma.jahan@dal.ca) or create an issue - https://github.com/SigmaJahan/Bug-Localization-IR-based-approaches-for-deep-learning-bugs/issues
