from dnn_model import dnn_model_kfold
from rvsm_model import rsvm_model
import time as time
import os
import json
from time import gmtime, strftime

def dnn(project, run_start_time):
    start = time.time()
    dump_file_folder = f"replication_results/{run_start_time}/{project}"
    if not os.path.isdir(dump_file_folder):
        os.makedirs(dump_file_folder, exist_ok = True)
    dump_file = os.path.join(dump_file_folder, "dnn_metrics.txt")

    metrics = dnn_model_kfold(project, 10)
    with open(dump_file, "w") as f:
        json.dump(metrics, f)

    print(f"DNN Competed for {project} in {time.time() - start}")
    return True


def rsvm(project, run_start_time):
    start = time.time()
    dump_file_folder = f"replication_results/{run_start_time}/{project}"
    if not os.path.isdir(dump_file_folder):
        os.makedirs(dump_file_folder, exist_ok = True)
    dump_file = os.path.join(dump_file_folder, "rsvm_metrics.txt")

    metrics = rsvm_model(project)
    with open(dump_file, "w") as f:
        json.dump(metrics, f)

    print(f"RSVM Competed for {project} in {time.time() - start}")
    return True

projects = ['tensorflow']
run_start_time = strftime("%Y-%m-%d %H-%M-%S", gmtime())
print(f"run_start_time", run_start_time)
result_path = f"replication_results/{run_start_time}/"
if not os.path.isdir(result_path):
    os.makedirs(result_path)

for project in projects:
    dnn(project, run_start_time)
    rsvm(project, run_start_time)
    