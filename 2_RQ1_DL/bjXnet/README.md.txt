# bjXnet: Bug Localization using Code Property Graphs and Attention Mechanism

## Overview
bjXnet is a deep learning-based bug localization technique that integrates Code Property Graph (CPG) with attention mechanisms. The framework uses a combination of Graph Neural Networks (GNNs) and Text Convolutional Neural Networks (TextCNNs) to encode the source code and bug reports, then employs an attention mechanism to localize buggy parts of the source code based on the bug reports.

## Features
- **Graph Encoder**: Uses GNN on CPG to encode code structure and relationships.
- **Text Encoder**: TextCNN to encode bug reports and source code files.
- **Attention Mechanism**: Focuses on critical parts of the code likely related to the reported bug.
- **Evaluation**: Supports evaluation using Accuracy, Mean Reciprocal Rank (MRR), and Mean Average Precision (MAP).

## Directory Structure
bjXnet/ │ ├── src/ │ ├── data_processing.py # Preprocess bug reports and source code │ ├── graph_encoder.py # Code Property Graph and GNN encoder │ ├── text_encoder.py # TextCNN for encoding bug reports and source code │ ├── attention_layer.py # Attention mechanism implementation │ ├── bjxnet_model.py # Full bjXnet model architecture │ ├── train.py # Training script │ ├── evaluate.py # Evaluation script │ └── utils.py # Utility functions │ ├── data/ │ ├── bug_reports/ # Folder for bug reports │ ├── source_code/ # Folder for source code │ └── cpg/ # Folder for CPG files │ ├── models/ # Folder to save trained models ├── results/ # Folder for evaluation results ├── requirements.txt # Required Python libraries └── README.md # Project setup and instructions

## Installation
To install the required dependencies, create a virtual environment and install the dependencies listed in `requirements.txt`:


# Create and activate a virtual environment
python3 -m venv env
source env/bin/activate  # For Linux/macOS
env\Scripts\activate  # For Windows

# Install dependencies
pip install -r requirements.txt

Usage
1. Preprocess Data
Ensure your bug reports, source code files, and CPG data are properly formatted. Use the data_processing.py to preprocess the data:

python src/data_processing.py

2. Train the Model
Train the bjXnet model using train.py:
python src/train.py
Modify the paths and dataset configurations inside train.py as needed.

3. Evaluate the Model
After training, evaluate the model using the evaluate.py script:
python src/evaluate.py
The results will be stored in the results/ directory.

Customizing the Model
To modify the model or its components, adjust the relevant files:
Graph Encoder: graph_encoder.py
Text Encoder: text_encoder.py
Attention Mechanism: attention_layer.py
Main Model Architecture: bjxnet_model.py