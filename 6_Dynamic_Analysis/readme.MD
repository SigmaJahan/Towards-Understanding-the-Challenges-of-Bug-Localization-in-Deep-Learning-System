# Replication Study on Bug Localization Approaches

## Overview
This repository contains a detailed replication study of three dynamic bug localization methods—DeepFD, DeepDiagnosis, and DeepLocalize—using their official replication packages on 21 real-world bugs. The results have been systematically analyzed and compared.

## Replicated Studies and Official Repositories
- [DeepFD](https://github.com/ArabelaTso/DeepFD)
- [DeepDiagnosis](https://github.com/DeepDiagnosis/ICSE2022)
- [DeepLocalize](https://github.com/Wardat-ISU/DeepLocalize)

## Methodology
### 1. Bug Selection
- Selected 21 real-world bugs from public GitHub issues related to prominent deep learning frameworks and projects (e.g., Keras, TensorFlow, MXNet).

### 2. Replication Procedure
- Followed the official guidelines provided by each repository.
- Utilized replication scripts and followed configuration instructions directly from the official repositories.
- Individually executed the official implementations on each bug to accurately replicate original experiments.

### 3. Result Recording
- Documented classification outcomes for each approach, clearly distinguishing between successful classifications and misclassifications based on the claimed capabilities of each method.

## Analysis
- Conducted a detailed comparative analysis for each method against each bug.
- Results are summarized and presented in the Excel file `dynamic_bug_localization_analysis.xlsx`, highlighting key strengths and limitations of each approach.

## Replication Findings
- **DeepFD** demonstrated effectiveness in identifying faults related to learning rates and optimizers but had limitations with dropout and data-related faults.
- **DeepDiagnosis** successfully diagnosed numerical anomalies using heuristic-driven approaches but had constraints with non-heuristic scenarios.
- **DeepLocalize** effectively localized numerical anomalies but struggled to classify faults not presenting numerical abnormalities.

Refer to the detailed Excel results (`dynamic_bug_localization_analysis.xlsx`) for more comprehensive insights.

The replication verified the claims of the original studies, clearly illustrating the capabilities and limitations of each bug localization approach. This documentation promotes transparency and reproducibility, facilitating future research efforts.