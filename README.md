[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

# Towards Understanding the Challenges of Bug Localization in Deep Learning Systems
This repository contains the data, experiments, and analysis for the EMSE 2025 journal paper "Towards Understanding the Challenges of Bug Localization in Deep Learning Systems".

---

## Abstract

Software bugs cost the global economy billions of dollars annually and claim \~50% of the programming time from software developers. Locating these bugs is crucial for their resolution but challenging. It is even more challenging in deep-learning systems due to their black-box nature. Bugs in these systems are also hidden not only in the code but also in the models and training data, which might make traditional debugging methods less effective. In this article, we conduct a large-scale empirical study to better understand the challenges of localizing bugs in deep-learning systems. First, we determine the bug localization performance of five existing techniques using 2,365 bugs from deep-learning systems and 2,913 from traditional software. We found these techniques significantly underperform in localizing deep-learning system bugs. Second, we evaluate how different bug types in deep learning systems impact bug localization. We found that the effectiveness of localization techniques varies with bug type due to their unique challenges. For example, tensor bugs were more accessible to locate due to their structural nature, while all techniques struggled with GPU bugs due to their external dependencies. Third, we investigate the impact of bugs' extrinsic nature on localization in deep-learning systems. We found that deep learning bugs are often extrinsic and thus connected to artifacts other than source code (e.g., GPU, training data), contributing to the poor performance of existing localization methods.

**[Read the Paper](./EMSE_2025_Final.pdf)**

---

## System Requirements

* **Operating System:** Windows 11, MacOS M2 or higher
* **Python Version:** 3.9
* **Development Environment:** VS Code

### Hardware (for different experiment phases):

* **Dataset Generation:** RAM: 16GB, GPU: Compute Canada Cedar
* **Scoring:** RAM: 16GB, GPU: Compute Canada Cedar
* **Experimental Results:** RAM: 16GB, GPU: Compute Canada Cedar

---

## Installation & Setup

### 1. Setting Up the Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # (or venv\Scripts\activate on Windows)
```

### 2. Installing Dependencies

```bash
pip install -r requirements.txt
```

* Each subfolder may provide its own requirements.txt. Install as needed.
* Jupyter Notebook is required for some analysis scripts.

---

## Dataset

* **Denchmark-BRs (Deep Learning Software Sysmtem - DLSW):** [https://github.com/RosePasta/Denchmark\_BRs](https://github.com/RosePasta/Denchmark_BRs)
* **BugGL-BRs (Non-Deep Learning Software Sysmtem - NDLSW):** [https://github.com/muvvasandeep/BuGL](https://github.com/muvvasandeep/BuGL)

---

## Project Structure
<details> <summary>Click to expand the full project structure</summary>
```
.
├── 1_RQ1_IR
│   ├── 1_dataset_generation
│   │   ├── a_git_download.py
│   │   ├── b_git_tags_extractor.py
│   │   ├── c_bug_repository_generator.py
│   │   ├── d_searchspace_generator.py
│   │   ├── e1_query_generator.py
│   │   ├── e2_query_generator_header.py
│   │   ├── f_file_class_method_variable_comment_generator.py
│   │   ├── g1_gtf_generator.py
│   │   ├── g2_gtf_generator_class_method_variable_comment.py
│   │   ├── h_commit_history_generator.py
│   │   ├── readme.md
│   │   ├── requirements.txt
│   │   └── z_config.txt
│   ├── 2_scoring
│   │   ├── a_similarity_models.py
│   │   ├── b_bug_sim.py
│   │   ├── c_code_structure_sim.py
│   │   ├── d_results_combination.py
│   │   ├── e_final_similarity_bluir.py
│   │   ├── f_final_similarity_buglocator.py
│   │   ├── g_strace_score.py
│   │   ├── h_commit_score_irbl.py
│   │   ├── readme.md
│   │   ├── requirements.txt
│   │   ├── util
│   │   │   └── ir_util.py
│   │   └── z_config.txt
│   ├── 3_experimental_results
│   │   ├── a_buglocator_bluir_data.py
│   │   ├── b_buglocator_bluir_result.py
│   │   ├── c_BLIA_data.py
│   │   ├── d_BLIA_result.py
│   │   ├── e_BLIA_Summarize.ipynb
│   │   ├── readme.md
│   │   ├── requirements.txt
│   │   ├── results_rq1_BLIA_BugGL.csv
│   │   ├── results_rq1_BLIA_Dechmark.csv
│   │   ├── results_rq1_buglocator_bluir_BugGL.csv
│   │   ├── results_rq1_buglocator_bluir_Denchmark.csv
│   │   ├── util
│   │   │   └── ir_util.py
│   │   └── z_config.txt
│   ├── 23icsme.yaml
│   ├── py
│   │   └── pyvenv.cfg
│   ├── pyvenv.cfg
│   ├── readme.md
│   └── requirements.txt
├── 1.1_RQ1
│   └── code_complexity_analysis.py
├── 2_RQ1_DL
│   ├── bjXnet
│   │   ├── bjXnet_result_dlsw.csv
│   │   ├── bjXnet_results_ndlsw.csv
│   │   ├── README.md.txt
│   │   ├── requirements.txt.txt
│   │   └── src
│   │       ├── attention_layer.py
│   │       ├── bjxnet_model.py
│   │       ├── cpg.py
│   │       ├── datapreprocessing.py
│   │       ├── evaluate.py
│   │       ├── graph_encoder.py
│   │       ├── text_encoder.py
│   │       ├── training.py
│   │       └── utils.py
│   └── DNNLOC
│       ├── 1_sample data
│       │   ├── features.csv
│       │   ├── pytorchlightning+pytorch-lightning_raw_cleaned.csv
│       │   ├── pytorchlightning+pytorch-lightning_raw_preprocessed.csv
│       │   ├── pytorchlightning+pytorch-lightning_raw_preprocessed.tsv
│       │   ├── pytorchlightning+pytorch-lightning_raw_preprocessed.txt
│       │   ├── pytorchlightning+pytorch-lightning_raw.csv
│       │   ├── tensorflow+tensorflow_raw_cleaned.csv
│       │   ├── tensorflow+tensorflow_raw_preprocessed.csv
│       │   ├── tensorflow+tensorflow_raw_preprocessed.tsv
│       │   └── tensorflow+tensorflow_raw.csv
│       ├── 2_data preprocessing
│       │   └── JSON_2_CSV_TSV_TXT.ipynb
│       ├── 3_src
│       │   ├── dnn_model.py
│       │   ├── dnn_model_org.py
│       │   ├── feature_extraction.py
│       │   ├── main.py
│       │   ├── main_org.py
│       │   ├── rvsm_model.py
│       │   └── util.py
│       ├── 4_sample result
│       │   ├── 2023-11-28 08-55-08
│       │   │   └── tensorflow
│       │   │       ├── dnn_metrics.txt
│       │   │       └── rsvm_metrics.txt
│       │   ├── 2023-11-28 08-55-46
│       │   │   └── tensorflow
│       │   │       ├── dnn_metrics.txt
│       │   │       └── rsvm_metrics.txt
│       │   └── 2023-11-28 08-58-08
│       │       └── tensorflow
│       │           ├── dnn_metrics.txt
│       │           └── rsvm_metrics.txt
│       ├── README.md
│       └── requirements.txt
├── 3_RQ2_RQ3_Analysis
│   ├── a_BuGL_Manual_Analysis_Mehil.xlsx
│   ├── a_BuGL_Manual_Analysis.xlsx
│   ├── b_Denchmark_Manual_Analysis_Mehil.xlsx
│   ├── b_Denchmark_Manual_Analysis.xlsx
│   ├── c_Correlation_Extrinsic_DL.ipynb
│   ├── d_Analysis_RQ2_RQ3.ipynb
│   └── e_Visualization.ipynb
│   └── emse_visualization_updated.py
├── 4_SBFL
│   ├── neuron_scores.pkl
│   ├── SBFL_Assessment_Log.log
│   ├── SBFL_Assessment.py
│   └── SBFL_Result.txt
├── 5_Visualization
│   └── EMSE_Visualization_Revision.ipynb
├── 6_Dynamic_Analysis
│   ├── dynamic_bug_localization_analysis.xlsx
│   └── readme.MD
├── EMSE_2025_Final.pdf
├── LICENSE
├── README.md
```
</details>
---

## RQ1: IR-based Bug Localization Methods

`1_RQ1_IR/1_dataset_generation/` contains scripts for:

1. Downloading and indexing DLSW/NDLSW projects
2. Tag extraction, bug repo organization, search space setup
3. Query generation (regex & header)
4. File/class/method/variable/comment extraction
5. Ground truth & commit history generation

`1_RQ1_IR/2_scoring/` contains IR-based scoring and ranking scripts:

* Compute similarity between bug reports and source files (rVSM, BLUiR, BugLocator, BRTracer, BLIA)
* Stack-trace & commit scoring
* Score combination scripts

`1_RQ1_IR/3_experimental_results/` scripts to evaluate models (Top\@K, MRR, MAP) and save results as .csv.

---

## RQ1: DL-based Bug Localization Methods

`DL_based_methods_RQ1/`

* **DNNLOC**:

  * Preprocessing scripts to convert Denchmark JSON to CSV/TSV
  * Source folder for feature extraction, training, evaluation
* **bjXnet**:

  * Source code for GNN-based approach (CPG, TextCNN, Attention, Training/Eval)

---

## RQ2 & RQ3: Manual Analysis, Modeling, and Human Study

`Manual_Analysis_RQ2_RQ3/`

* Manual annotation (Excel/CSV) for both Denchmark and BugGL datasets
* Jupyter notebooks for correlation and RQ2/RQ3 analysis

`1.2_RQ2/` and `1.3_RQ3/` contain Python scripts for:

* Data labeling, inter-rater agreement, model training (RQ2)
* Survey/developer study, human-in-the-loop evaluation (RQ3)

---

## Dynamic Analysis

* Conducted a detailed comparative analysis for each method against each bug.

* Results are summarized and presented in the Excel file dynamic_bug_localization_analysis.xlsx, highlighting key strengths and limitations of each approach.

## Main Scripts & Notebooks

* For IR-based methods: see scripts in `1_RQ1_IR/1_dataset_generation/` and `1_RQ1_IR/2_scoring/`
* For DL-based methods: see `DL_based_methods_RQ1/DNNLOC/` and `DL_based_methods_RQ1/bjXnet/`
* For manual/correlation analysis: see `Manual_Analysis_RQ2_RQ3/`

---

## Citation

If you use this code or dataset, please cite our paper:

```bibtex
@article{Jahan2025BugLoc,
  author  = {Sigma Jahan and Mehil B. Shah and Mohammad Masudur Rahman},
  title   = {Towards Understanding the Challenges of Bug Localization in Deep Learning Systems},
  journal = {Empirical Software Engineering},
  year    = {2025},
}
```

---

## License

This repo is released under the MIT License. See [LICENSE](LICENSE).

---

## Contact

For questions, email [sigma.jahan@dal.ca](mailto:sigma.jahan@dal.ca)

---

## Acknowledgment & References

During the implementation of our study, we have referred to the following Github repositories:

1. [https://github.com/RosePasta/IRBL\_for\_DLSW](https://github.com/RosePasta/IRBL_for_DLSW)
2. [https://github.com/RosePasta/Denchmark\_BRs](https://github.com/RosePasta/Denchmark_BRs)
3. [https://github.com/muvvasandeep/BuGL](https://github.com/muvvasandeep/BuGL)
4. [https://github.com/exatoa/Bench4BL](https://github.com/exatoa/Bench4BL)
5. [https://github.com/klausyoum/BLIA](https://github.com/klausyoum/BLIA)
6. [https://github.com/joernio/joern/tree/master](https://github.com/joernio/joern/tree/master)
7. [DeepFD](https://github.com/ArabelaTso/DeepFD)
8. [DeepDiagnosis](https://github.com/DeepDiagnosis/ICSE2022)
9. [DeepLocalize](https://github.com/Wardat-ISU/DeepLocalize)
