from util import csv2dict, tsv2dict, helper_collections, topk_accuarcy
from sklearn.neural_network import MLPRegressor
import joblib
from joblib import Parallel, delayed, cpu_count
from ray.util.joblib import register_ray
from math import ceil
import numpy as np
import os
import ray
import joblib

register_ray()

def oversample(samples):
    """ Oversamples the features for label "1" 
    
    Arguments:
        samples {list} -- samples from features.csv
    """
    samples_ = []

    # oversample features of buggy files
    for i, sample in enumerate(samples):
        samples_.append(sample)
        if i % 51 == 0:
            for _ in range(9):
                samples_.append(sample)

    return samples_


def features_and_labels(samples):
    """ Returns features and labels for the given list of samples
    
    Arguments:
        samples {list} -- samples from features.csv
    """
    features = np.zeros((len(samples), 5))
    labels = np.zeros((len(samples), 1))

    for i, sample in enumerate(samples):
        features[i][0] = float(sample["rVSM_similarity"])
        features[i][1] = float(sample["collab_filter"])
        features[i][2] = float(sample["classname_similarity"])
        features[i][3] = float(sample["bug_recency"])
        features[i][4] = float(sample["bug_frequency"])
        labels[i] = float(sample["match"])

    return features, labels


def kfold_split_indexes(k, len_samples):
    """ Returns list of tuples for split start(inclusive) and 
        finish(exclusive) indexes.
    
    Arguments:
        k {integer} -- the number of folds
        len_samples {interger} -- the length of the sample list
    """
    step = ceil(len_samples / k)
    ret_list = [(start, start + step) for start in range(0, len_samples, step)]

    return ret_list


def kfold_split(bug_reports, samples, start, finish):
    """ Returns train samples and bug reports for test
    
    Arguments:
        bug_reports {list of dictionaries} -- list of all bug reports
        samples {list} -- samples from features.csv
        start {integer} -- start index for test fold
        finish {integer} -- start index for test fold
    """
    train_samples = samples[:start] + samples[finish:]
    test_samples = samples[start:finish]

    test_br_ids = set([s["report_id"] for s in test_samples])
    test_bug_reports = [br for br in bug_reports if br["id"] in test_br_ids]

    return train_samples, test_bug_reports


def train_dnn(
    project, i, num_folds, samples, start, finish, sample_dict, bug_reports, br2files_dict):
    """ Trains the dnn model and calculates top-k accuarcies
    
    Arguments:
        i {interger} -- current fold number for printing information
        num_folds {integer} -- total fold number for printing information
        samples {list} -- samples from features.csv
        start {integer} -- start index for test fold
        finish {integer} -- start index for test fold
        sample_dict {dictionary of dictionaries} -- a helper collection for fast accuracy calculation
        bug_reports {list of dictionaries} -- list of all bug reports
        br2files_dict {dictionary} -- dictionary for "bug report id - list of all related files in features.csv" pairs
    """
    print("Fold: {} / {}".format(i + 1, num_folds), end="\r")

    train_samples, test_bug_reports = kfold_split(bug_reports, samples, start, finish)
    # print training samples before oversampling
    print("Train samples before oversampling: {}, Test samples: {}".format(len(train_samples), len(test_bug_reports)))
    train_samples = oversample(train_samples)
    train_samples_print = oversample(train_samples)
    # print training samples after oversampling
    print("Train samples after oversampling: {}, Test samples: {}".format(len(train_samples_print), len(test_bug_reports)))
    np.random.shuffle(train_samples)
    X_train, y_train = features_and_labels(train_samples)
    clf = MLPRegressor(
        solver="sgd",
        alpha=1e-5,
        hidden_layer_sizes=(300,),
        random_state=1,
        max_iter=10000,
        n_iter_no_change=30,
    )

    with joblib.parallel_backend('ray'):
       clf.fit(X_train, y_train.ravel())

    acc_dict, map_value, mrr_value = topk_accuarcy(test_bug_reports, sample_dict, br2files_dict, clf=clf)

    return acc_dict, map_value, mrr_value


def dnn_model_kfold(project, k=10):
    """ Run kfold cross validation sequentially
    
    Keyword Arguments:
        k {integer} -- the number of folds (default: {10})
    """
    samples = csv2dict("D:\\Bug-Localization-using-DNN-rVSM-for-deep-learning-bugs\\data\\features.csv")
    br_file_path = "D:\\Bug-Localization-using-DNN-rVSM-for-deep-learning-bugs\\data\\tensorflow+tensorflow_raw_preprocessed.tsv"
    
    sample_dict, bug_reports, br2files_dict = helper_collections(samples, br_file_path)

    np.random.shuffle(samples)
    samples_len = len(samples)
    print(samples_len)

    metrics = []
    for i, (start, step) in enumerate(kfold_split_indexes(k, samples_len)):
        acc_dict, map_value, mrr_value = train_dnn(project, i, k, samples, start, start + step, sample_dict, bug_reports, br2files_dict)
        
        # Create a dictionary for each fold's metrics and append to the list
        fold_metrics = {
            "accuracy": acc_dict,
            "avg_map": map_value,
            "avg_mrr": mrr_value
        }
        metrics.append(fold_metrics)

    # print metrics
    print("Accuracy Accuracy:", metrics[9]["accuracy"])
    print("Average MAP Score:", metrics[9]["avg_map"])
    print("Average MRR Score:", metrics[9]["avg_mrr"])

    # Calculate averages
    avg_acc_dict = {i: 0 for i in range(1, 21)}
    avg_map = 0
    avg_mrr = 0
    for metric in metrics:
        for key, value in metric["accuracy"].items():
            avg_acc_dict[key] += value
        avg_map += metric["avg_map"]
        avg_mrr += metric["avg_mrr"]

    # Final averaging
    avg_acc_dict = {key: round(value / k, 3) for key, value in avg_acc_dict.items()}
    avg_map = round(avg_map / k, 3)
    avg_mrr = round(avg_mrr / k, 3)

    print("Accuracy Accuracy_after:", avg_acc_dict)
    print("Average MAP Score_after:", avg_map)
    print("Average MRR Score_after:", avg_mrr)


    return {
        "accuracy": avg_acc_dict,
        "avg_mrr": avg_mrr,
        "avg_map": avg_map
    }