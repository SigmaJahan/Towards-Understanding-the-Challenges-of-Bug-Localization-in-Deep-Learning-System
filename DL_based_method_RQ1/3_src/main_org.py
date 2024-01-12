from dnn_model import dnn_model_kfold
from rvsm_model import rsvm_model

# Print with the appropriate model name `DNN` or `RVSM

print("DNN result: " + str(dnn_model_kfold(10)))
print("RVSM result: " + str(rsvm_model()))