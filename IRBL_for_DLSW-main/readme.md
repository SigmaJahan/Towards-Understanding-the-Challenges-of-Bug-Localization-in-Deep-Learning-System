# Bug Localization for Deep Learning software bugs
This repository is a reproduction package for bug localization for deep learning software projects.

## Preparation
- Environments: Python 3.8 + 22icst.yaml
- Download Denchmark-BRs
    - https://github.com/RosePasta/Denchmark_BRs
## Structure
Each folder information is provided on Readme.md of each folder.

```
IRBL for DLSW
│   README.md
│   22icst.yaml
└───1_dataset_generation
└───2_scoring
└───3_experimental_results
```

These folders consist of Python files for the tasks below.

## 1_dataset_generation
1) download git repository and extract released versions
2) generate bug reports and search space (both source files and functions)
3) extract specific textual information by regular expression and HTML header
4) preprocess the bug report for query
5) preprocess source files/functions for search space
6) generate ground truth files and (class, method, variable & comment)

## 2_scoring
1) Compute the similarity between bug reports and source files by three IR models (sf_sim - VSM, rVSM, BM25)
    - rVSM reference: Where should the bugs be fixed? more accurate information retrieval-based bug localization based on bug reports, ICSE'12
2) Compute the similarity between a bug report and historical bug reports (br_sim)
    - reference: Where should the bugs be fixed? more accurate information retrieval-based bug localization based on bug reports, ICSE'12
3) Compute code structure score - method, class, variable, comment scores individually - BluiR Reference: Improving Bug Localization using Structured Information Retrieval (ASE 2013)
4) Combines the scores from method, class, variable, comment and sum them together for each source file.
5) Combines similarity score from a_similarity_models.py (sf_sim), similarity score from e_bug_sim.py (br_sim) and similarity score from h_results_combination.py (bm25_final) for the BluiR methodology.
6) Combines the similarity score from a_similarity_models.py (sf_sim) and similarity score from e_bug_sim.py (br_sim) and use the euqation from the paper for BugLocator methodology.

## 3_experimental results
1) Finding the result of BluiR and Buglocator using MRR, MAP, Top@5,Top@10, Top@20, Top@50, Top@100

