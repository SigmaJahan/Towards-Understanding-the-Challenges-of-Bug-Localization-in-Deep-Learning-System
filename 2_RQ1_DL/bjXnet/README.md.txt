# bjXnet: Bug Localization using Code Property Graphs and Attention Mechanism

## Overview
bjXnet is a deep learning-based bug localization technique that integrates Code Property Graph (CPG) with attention mechanisms. The framework uses a combination of Graph Neural Networks and Text Convolutional Neural Networks to encode the source code and bug reports, then employs an attention mechanism to localize buggy parts of the source code based on the bug reports.


## Features
- Graph Encoder: Uses GNN on CPG to encode code structure and relationships.
- Text Encoder: TextCNN to encode bug reports and source code files.
- Attention Mechanism: Focuses on critical parts of the code likely related to the reported bug.
- Evaluation: Supports evaluation using Accuracy, Mean Reciprocal Rank (MRR), and Mean Average Precision (MAP).

## Directory Structure
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


## Installation
To install the required dependencies, create a virtual environment and install the dependencies listed in `requirements.txt`:

## Generating the Code Property Graph (CPG)
To generate the Code Property Graph (CPG) from the source code, follow these steps using **Joern**.

### 1. Install Joern
git clone https://github.com/joernio/joern.git
cd joern
./build.sh
./joern-install.sh
export PATH=$PATH:/path_to_joern/bin/

### 2.  Generate the CPG
Once Joern is installed, it can be used to generate a CPG for the source code.
cd /path_to_your_source_code_directory/
joern-parse --output cpg.bin .

### 3. Load and Query the CPG
To interact with the generated CPG, Joern shell can be launched:
joern
cpg = cpgLoader.load("/path_to_your_source_code_directory/cpg.bin")
cpg.method.name.p

### 4. Automate CPG Generation with Python
If to automate the CPG extraction, use the Python script inside src/cpg.py

# Create and activate a virtual environment
python3 -m venv env
env\Scripts\activate 

# Install dependencies
pip install -r requirements.txt

Usage
1. Preprocess Data
Ensure your bug reports, source code files, and CPG data are properly formatted. Use the data_processing.py to preprocess the data:
python src/data_processing.py

2. Train the Model
Train the bjXnet model using train.py: python src/train.py
Modify the paths and dataset configurations inside train.py as needed.

3. Evaluate the Model
After training, evaluate the model using the evaluate.py script: python src/evaluate.py