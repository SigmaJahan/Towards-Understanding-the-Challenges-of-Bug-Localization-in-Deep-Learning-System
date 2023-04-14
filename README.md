# ICSME-2023-Bug-Localization
This repository serves as the code repository for the ICSME 2023 submission concerning Bug Localization for Deep Learning Bugs. Detailed steps are can be found inside each section.

## Preparation
- Environments: Python 3.8 + 22icst.yaml
- Download Denchmark-BRs
    - https://github.com/RosePasta/Denchmark_BRs
## Structure
Each folder information is provided on Readme.md of each folder.


## IR_based_methods_RQ1_DLSW

IRBL for DLSW
│   README.md
│   22icst.yaml
└───1_dataset_generation_new
└───2_scoring
└───3_experimental_results

These folders consist of Python files for the tasks below.

a) 1_dataset_generation

1) download git repository and extract released versions
2) generate bug reports and search space (both source files and functions)
3) extract specific textual information by regular expression and HTML header
4) preprocess the bug report for query
5) preprocess source files for search space (only used Python file) 
6) generate ground truth files and (class, method, variable & comment)
7) generate commit history

b) 2_scoring

1) Compute the similarity between bug reports and source files with rVSM (sf_sim)
    - sf_sim with rVSM reference: Where should the bugs be fixed? more accurate information retrieval-based bug localization based on bug reports, ICSE'12
2) Compute the similarity between a bug report and historical bug reports (br_sim)
    - br_sim reference: Where should the bugs be fixed? more accurate information retrieval-based bug localization based on bug reports, ICSE'12
3) Compute code structure score - method, class, variable, comment scores individually 
    - BLUiR Reference: Improving Bug Localization using Structured Information Retrieval (ASE 2013)
4) Combines the scores from method, class, variable, comment and sum them together for each source file.
5) Combines similarity score from a_similarity_models.py (sf_sim), similarity score from e_bug_sim.py (br_sim) and similarity score from h_results_combination.py (bm25_final) for the BluiR methodology.
6) Combines the similarity score from a_similarity_models.py (sf_sim) and similarity score from e_bug_sim.py (br_sim) and use the euqation from the paper for BugLocator methodology.
7) Compute the stack trace score
8) Compute the commit score 
   - BLIA Reference: Improved bug localization based on code change histories and bug reports, IST'17

c) 3_experimental results

1) Evaluating Buglocator, BLUiR and BLIA using MRR, MAP, Top@1, Top@5, Top@10

## Manual_analysis_all_ICSME.ipynb 

This includes the dataset of manual analysis and generating results from the manual analysis for RQ2 & RQ3 

