from util import csv2dict, tsv2dict, helper_collections, topk_accuarcy
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split, KFold
import numpy as np


def rsvm_model(project):
    samples = csv2dict("D:\\Bug-Localization-using-DNN-rVSM-for-deep-learning-bugs\\data\\features.csv")
    rvsm_list = [float(sample["rVSM_similarity"]) for sample in samples]

    br_file_path = " D:\\Bug-Localization-using-DNN-rVSM-for-deep-learning-bugs\\data\\tensorflow+tensorflow_raw_preprocessed.tsv"
    sample_dict, bug_reports, br2files_dict = helper_collections(samples, br_file_path, True)

    acc_dict, avg_map, avg_mrr = topk_accuarcy(bug_reports, sample_dict, br2files_dict)

    return {
        "accuracy": acc_dict,
        "avg_mrr": avg_mrr,
        "avg_map": avg_map
    }