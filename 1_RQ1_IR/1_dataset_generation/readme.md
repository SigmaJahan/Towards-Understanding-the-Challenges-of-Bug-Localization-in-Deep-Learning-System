# Dataset generation
This folder consists of python files for data preparation and generation for IRBL.


## Steps
1. Setting the absolute path in _z_config.txt_
    - The paths that require data in advance are _denchmark_path_, _hunk_path_, and _locus_commit_path_.
    -  The rest is where the data is generated after the python files are run.

2. Download Denchmark-BRs and move the packages in _denchmark_path_ in _z_config_
    - https://github.com/RosePasta/Denchmark_BRs

3. Execute step by step from a_... to h_... Python files. 
    1) **a_git_download.py**: Download DLSW projects based on Denchmark (output: _git_path_)
    2) **b_git_tags_extractor.py**: Collect project versions based on Tag info. (output: _tag_path_)
    3) **c_bug_repository_generator.py**: Divide the bug reports by relevant project version (output: _bug_path_)
    4) **d_searchspace_generator.py**: Set the search space by relevant proejct version (= divide the all files by relevant project version) (output: _searchspace_path_)
        - You may need to install below.
        ```        
        pip install pyhumps
        pip install camelsplit
        pip install nltk
        python
        import nltk
        nltk.download('stopwords')
        nltk.download('punkt')
        ```
    5) **e1_query_generator.py**: Generate query based on regular expression (output: _query_path_)
    6) **e2_query_generator_header.py**: Generate query based on HTML header (output: _query_path_)
    8) **f_file_class_method_variable_comment_generator.py**: Index source files, class, method, variable and comment (output: file_path, class_path, function_path, variable_path, comment_path)
    9) **g1_gtf_generator.py**: Generate ground truth source files (output: _gtf_path))
    10) **g2_gtf_generator_class_method_variable_comment.py**: Generate groud truth for class, methods, variable, comments (output: _gtf_path_) (e.g., %bug_id%_method.txt)
    11) **h_commit_history_generator.py**: Generate commit history (outout: commit_path)
            
