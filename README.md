# Towards Automated Localization of Deep Learning Bugs

# Project Description 
**Abstract:** Software bugs (errors in computer programs) cost the global economy trillions of dollars annually and claim ~50\% of the programming time from software developers. One of the crucial steps toward correcting a bug is pinpointing its location within the software code,  which is a challenging task. The task is even more challenging with deep learning applications due to their black-box nature. Unlike traditional software bugs, the bugs in deep learning applications are hidden not only in the code but also in the models and training data. Thus, despite decades of research, traditional debugging methods might not be adequate for deep learning bugs due to their unique challenges. Given the rapid growth in deep learning applications, an automated approach for detecting deep learning bugs is highly warranted. The proposed research aims to (a) comprehensively assess the feasibility of traditional debugging methods for detecting deep learning bugs, (b) manual analysis of deep learning software bugs, and (c) gain a deeper understanding of the implication of extrinsic and intrinsic bugs. Recent incidents suggest that deep learning bugs could be costly and fatal (e.g., the Uber SUV accident in Arizona and the Tesla autopilot crash). The proposed research might significantly change the status quo. Our work provides important empirical evidence and actionable insights on deep learning bugs to advance academic research for automated software debugging.  

## Preparation
- Environments: Python 3.9 
- Install Jupyter Notebook
- We have dependencies stated in the 23icsme.yaml file
- Each folder information is provided on Readme.md and requirements.txt of each folder
- Install python libraries $ pip install -r scripts/requirements.txt (Provided in each folder)

## Dataset
- Download Denchmark-BRs (DLSW)
    - https://github.com/RosePasta/Denchmark_BRs
- Download BugGL-BRs (NDLSW)
    - https://github.com/muvvasandeep/BuGL

## IR_based_methods_RQ1_DLSW
```
IRBL for DLSW
│   README.md
│   23icsme.yaml
└───1_dataset_generation
└───2_scoring
└───3_experimental_results
```
These folders consist of Python files/Jupyter Notebook for the tasks below.

** 1_dataset_generation **

1) download git repository and extract released versions
2) generate bug reports and search space (both source files and functions)
3) extract specific textual information by regular expression and HTML header
4) preprocess the bug report for query
5) preprocess source files for search space (only used Python file) 
6) generate ground truth files and (class, method, variable & comment)
7) generate commit history

** 2_scoring **

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

** 3_experimental results **

1) Evaluating Buglocator, BLUiR and BLIA using MRR, MAP, Top@1, Top@5, Top@10

## Manual_analysis_all_ICSME.ipynb 

This includes the dataset of manual analysis and generating results from the manual analysis for RQ2 & RQ3 

# Contributor
Sigma Jahan (sigma.jahan@dal.ca)

# Licensing Information

https://www.freecodecamp.org/news/how-open-source-licenses-work-and-how-to-add-them-to-your-projects-34310c3cf94/

(Can get after creating the repo on Github) - Use Apache License 2.0, MIT license, General Public License as you wish

# Something not working as expected?

**Contact:** Sigma Jahan (sigma.jahan@dal.ca) or create an issue
