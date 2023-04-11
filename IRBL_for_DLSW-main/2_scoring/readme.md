# Dataset generation
This folder consists of python files for getting the similarity scores between the query and the source files.

## Steps
1. Setting the absolute path in _z_config.txt_
    - Just copy and paste a set of paths from the 1_dataset_generation folder z_config.
2. You may need to install below.
    ```
	pip install sklearn
	pip install rank-bm25
    ```
3. Execute step by step from a_... to g_... Python files. 
    1) **a_similarity_models.py**: Compute similarity between a bug report and source files. (output: _irbl_path/repo/bug_id/sf_sim/_)
    2) **b_bug_sim.py**: Compute  simliarity between a bug report and relevant past bug reports and their fixed source files (output: _irbl_path/repo/bug_id/br_sim/_)
    3) **c_code_structure_sim.py**: Compute method, class, variable, comment scores individually (output: _irbl_path/repo/bug_id/mth_sim/python_bm25_method.txt/ or python_bm25_class.txt or python_bm25_variable.txt or python_25_comments.txt)
    4) **d_results_combination.py** : Combines the scores from method, class, variable, comment and sum them together for each source file. (output:_irbl_path/repo/bug_id/bm25_final.txt/_)
    5) **e_final_similarity_bluir.py** : Combines similarity score from a_similarity_models.py (sf_sim), similarity score from e_bug_sim.py (br_sim) and similarity score from h_results_combination.py (bm25_final) for the BluiR methodology. 
    6) **f_final_similarity_buglocator.py**: Combines the similarity score from a_similarity_models.py (sf_sim) and similarity score from e_bug_sim.py (br_sim) and use the euqation from the paper for BugLocator methodology.
    7) **g_strace_score.py** : Compute similarity between bug report and stack trace
    8) **h_commit_score_irbl.py**: Compute similarity with commit history
    
