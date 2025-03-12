import matplotlib
matplotlib.use("Agg")
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import sys
import pickle
from collections import defaultdict
from tensorflow.keras import layers, models, Input
import warnings
warnings.filterwarnings("ignore")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.handlers.clear()

console_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("debug_output3.log", mode="w")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logging.getLogger("matplotlib.font_manager").setLevel(logging.WARNING)

np.random.seed(42)
tf.random.set_seed(42)
(x_train, y_train), _ = tf.keras.datasets.cifar100.load_data()
x_train = x_train / 255.0

SUBSAMPLE_SIZE = 5000
x_train, y_train = x_train[:SUBSAMPLE_SIZE], y_train[:SUBSAMPLE_SIZE]
logger.debug(f"x_train shape: {x_train.shape}, y_train shape: {y_train.shape}")

NUM_RUNS = 20
EPOCHS = 10
PATIENCE = 3
FAIL_THRESHOLD = 0.01

def create_model():
    """
    CNN with a known fault: final Dense layer missing softmax activation.
    Named "faulty_output" for clarity.
    """
    model = models.Sequential([
        Input(shape=(32, 32, 3), name="input_layer"),
        layers.Conv2D(64, (3, 3), padding="same", activation='relu', name="conv2d_1"),
        layers.Conv2D(64, (3, 3), padding="same", activation='relu', name="conv2d_2"),
        layers.MaxPooling2D((2, 2), name="maxpool_1"),
        layers.Conv2D(128, (3, 3), padding="same", activation='relu', name="conv2d_3"),
        layers.Conv2D(128, (3, 3), padding="same", activation='relu', name="conv2d_4"),
        layers.MaxPooling2D((2, 2), name="maxpool_2"),
        layers.Flatten(name="flatten"),
        layers.Dense(256, activation='relu', name="dense_1"),
        layers.Dense(128, activation='relu', name="dense_2"),
        layers.Dense(100, activation=None, name="faulty_output"),  # <-- fault
    ])
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'],
    )
    return model


def is_training_failed(history):
    """
    Return True if (average of last PATIENCE epochs) - (min of last PATIENCE) < FAIL_THRESHOLD
    """
    loss_list = history.history["loss"]
    logger.debug(f"Training loss history: {loss_list}")
    if len(loss_list) < PATIENCE:
        return False
    window = loss_list[-PATIENCE:]
    return (np.mean(window) - np.min(window)) < FAIL_THRESHOLD


class NeuronCoverageCallback(tf.keras.callbacks.Callback):
    """
    - Collect coverage (activation > 0) for each layer & epoch.
    - Store in self.activations[layer_name][epoch] = coverage_vector (shape == (#neurons,))
    """
    def __init__(self, sample_data):
        super().__init__()
        self.sample_data = sample_data
        self.activations = defaultdict(list)

    def on_train_begin(self, logs=None):
        try:
            _ = self.model.predict(self.sample_data[:1])
        except Exception as e:
            logger.error("Error forcing forward pass: %s", e)

        # Identify which layers to track
        self.layer_outputs = []
        self.layer_names = []
        for layer in self.model.layers:
            if isinstance(layer, (layers.Conv2D, layers.Dense)):
                self.layer_outputs.append(layer.output)
                self.layer_names.append(layer.name)
                logger.debug(f"Tracking layer: {layer.name}")

        try:
            self.activation_model = tf.keras.Model(
                inputs=self.model.inputs, outputs=self.layer_outputs
            )
        except Exception as e:
            logger.error("Error creating activation model: %s", e)

    def on_epoch_end(self, epoch, logs=None):
        # Evaluate coverage on a small subset
        batch = self.sample_data[:200]
        try:
            acts = self.activation_model.predict(batch)
            if not isinstance(acts, list):
                acts = [acts]
            for layer_name, act in zip(self.layer_names, acts):
                # Flatten spatial dims => (batch_size, #neurons)
                mask = (act > 0).reshape(act.shape[0], -1).astype(float)
                # coverage_vector: fraction of samples that activate each neuron
                coverage_vector = np.mean(mask, axis=0)  # shape (num_neurons,)
                self.activations[layer_name].append(coverage_vector)
        except Exception as e:
            logger.error("Error extracting coverage at epoch end: %s", e)


test_outcomes = []  # True => fail, False => pass

# For final coverage after training, we store:
# -- "binary" coverage at the layer-level (1/0)
# -- average coverage (i.e. mean of neuron coverage) at the layer-level for distribution
layer_binary_coverage = defaultdict(list)  # {layer_name: [1 or 0 per run]}
layer_avg_coverage = defaultdict(list)     # {layer_name: [float per run]}

# For neuron-level coverage:
neuron_coverage_data = defaultdict(dict)   # {layer_name: {run_id: (num_neurons,) coverage}}

results_lines = []
dummy_model = create_model()
tracked_layers = []
for layer in dummy_model.layers:
    if isinstance(layer, (layers.Conv2D, layers.Dense)):
        tracked_layers.append(layer.name)
for run_id in range(NUM_RUNS):
    logger.debug(f"Starting run {run_id+1}/{NUM_RUNS}")
    tf.random.set_seed(run_id)
    np.random.seed(run_id)

    model = create_model()
    coverage_cb = NeuronCoverageCallback(sample_data=x_train)

    history = model.fit(
        x_train, y_train,
        epochs=EPOCHS,
        batch_size=8,
        verbose=1,
        callbacks=[coverage_cb]
    )

    failed = is_training_failed(history)
    test_outcomes.append(failed)

    # Combine coverage across epochs => final coverage for each layer
    for layer_name in coverage_cb.layer_names:
        # coverage_cb.activations[layer_name] = list of coverage_vectors (one per epoch)
        if len(coverage_cb.activations[layer_name]) == 0:
            coverage_vec = None
        else:
            # average across epochs -> shape (num_neurons,)
            coverage_vec = np.mean(coverage_cb.activations[layer_name], axis=0)

        neuron_coverage_data[layer_name][run_id] = coverage_vec

        # layer-level coverage:
        if coverage_vec is None:
            layer_binary_coverage[layer_name].append(0)
            layer_avg_coverage[layer_name].append(0.0)
        else:
            # 1) binary coverage: if ANY neuron > 0 coverage
            if np.any(coverage_vec > 0.0):
                layer_binary_coverage[layer_name].append(1)
            else:
                layer_binary_coverage[layer_name].append(0)

            # 2) average coverage: mean fraction of samples that activated each neuron
            avg_cov = float(np.mean(coverage_vec))
            layer_avg_coverage[layer_name].append(avg_cov)

    line = f"Run {run_id+1}/{NUM_RUNS} -> {'Failed' if failed else 'Passed'}"
    print(line)
    results_lines.append(line)

num_failed = sum(test_outcomes)
num_passed = NUM_RUNS - num_failed

summary_line = (
    f"\nPass/Fail Summary:\n"
    f"Total Runs: {NUM_RUNS}, Failed: {num_failed}, Passed: {num_passed}\n"
)
print(summary_line)
results_lines.append(summary_line)

if num_failed == 0 or num_passed == 0:
    warn_line = (
        "All runs are either pass or fail. Tarantula suspiciousness is not meaningful.\n"
    )
    print(warn_line)
    results_lines.append(warn_line)
else:
    def tarantula_layer_scores(binary_coverage, outcomes):
        """
        binary_coverage[layer_name] = [1 or 0 per run]
        outcomes = list of bool, True if fail
        """
        scores = {}
        for layer_name, cov_list in binary_coverage.items():
            fail_cov = sum(1 for i, c in enumerate(cov_list) if c == 1 and outcomes[i])
            pass_cov = sum(1 for i, c in enumerate(cov_list) if c == 1 and not outcomes[i])
            # Tarantula formula
            top = fail_cov / num_failed if num_failed > 0 else 0
            bot = (fail_cov / num_failed) + (pass_cov / num_passed) if (num_failed > 0 and num_passed > 0) else 1
            score = top / bot if bot > 0 else 0.0
            scores[layer_name] = score
        return scores

    # --------------------------------------------------------------
    # 11.2) Tarantula for Neurons
    # --------------------------------------------------------------
    def tarantula_neuron_scores(ncov_dict, outcomes):
        """
        ncov_dict[layer_name][run_id] = coverage_vec (num_neurons,) in [0,1].
        We'll call a neuron "covered" if coverage_vec[neuron_idx] > 0 for that run.
        """
        from collections import defaultdict
        scores = defaultdict(dict)
        for layer_name in ncov_dict:
            runs_dict = ncov_dict[layer_name]  # {run_id: coverage_vec or None}
            if len(runs_dict) == 0:
                continue

            valid_run_ids = [r for r in runs_dict if runs_dict[r] is not None]
            if not valid_run_ids:
                continue

            # pick a sample run to see how many neurons
            sample_run_id = valid_run_ids[0]
            num_neurons = len(runs_dict[sample_run_id])

            for neuron_idx in range(num_neurons):
                fail_cov = 0
                pass_cov = 0
                for r_id in runs_dict:
                    cov_vec = runs_dict[r_id]
                    if cov_vec is None:
                        continue
                    if cov_vec[neuron_idx] > 0:
                        if outcomes[r_id]:
                            fail_cov += 1
                        else:
                            pass_cov += 1
                # Tarantula
                top = fail_cov / num_failed if num_failed > 0 else 0
                bot = (fail_cov / num_failed) + (pass_cov / num_passed) if (num_failed > 0 and num_passed > 0) else 1
                score = top / bot if bot > 0 else 0.0
                scores[layer_name][neuron_idx] = score

        return scores

    layer_scores = tarantula_layer_scores(layer_binary_coverage, test_outcomes)
    neuron_scores = tarantula_neuron_scores(neuron_coverage_data, test_outcomes)

    print("Layer-Level Tarantula Scores:")
    results_lines.append("Layer-Level Tarantula Scores:")
    
    #print avg neuron coverage for each layer
    for layer_name in neuron_coverage_data:
        if len(neuron_coverage_data[layer_name]) == 0:
            continue
        avg_cov = np.mean([v for v in neuron_coverage_data[layer_name].values() if v is not None])
        print(f"  {layer_name}: {avg_cov:.4f}")
        results_lines.append(f"  {layer_name}: {avg_cov:.4f}")
        
    #

    # Sort by descending suspiciousness
    sorted_layer_names = sorted(layer_scores.keys(), key=lambda ln: layer_scores[ln], reverse=True)
    for ln in sorted_layer_names:
        line = f"  {ln}: {layer_scores[ln]:.4f}"
        print(line)
        results_lines.append(line)

    plt.figure(figsize=(10, 6))
    y_vals = [layer_scores[ln] for ln in sorted_layer_names]
    bars = plt.barh(range(len(y_vals)), y_vals, align='center')
    plt.yticks(range(len(y_vals)), sorted_layer_names)
    plt.xlabel("Suspiciousness Score")
    plt.title("Layer-Level Tarantula Scores")
    for bar, score in zip(bars, y_vals):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
                 f"{score:.4f}", va="center", ha="left")
    plt.tight_layout()
    plt.savefig("layer_tarantula_scores.png")
    plt.close()

    for rank, layer_name in enumerate(sorted_layer_names, start=1):
        if layer_name == "faulty_output":
            msg = (
                f"\n'faulty_output' layer is ranked {rank} "
                f"out of {len(sorted_layer_names)} by Tarantula suspiciousness.\n"
            )
            print(msg)
            results_lines.append(msg)
            break

    if "faulty_output" in neuron_scores:
        final_scores = neuron_scores["faulty_output"]
        # Sort neurons by descending suspiciousness
        sorted_neurons = sorted(final_scores.keys(), key=lambda idx: final_scores[idx], reverse=True)

        explanation = (
            "\nNeuron-Level Tarantula Scores for 'faulty_output' (Top 10):\n"
            "Note: 'faulty_output' has 100 neurons (indexes 0..99). The index listed\n"
            "corresponds to that neuron's position in the final Dense layer.\n"
        )
        print(explanation)
        results_lines.append(explanation)

        for i, neuron_idx in enumerate(sorted_neurons[:10], start=1):
            s = final_scores[neuron_idx]
            line = f"  {i}. [faulty_output] Neuron {neuron_idx}: {s:.4f}"
            print(line)
            results_lines.append(line)
            
        x_vals = sorted_neurons
        y_vals = [final_scores[n] for n in x_vals]
        plt.figure(figsize=(10, 6))
        plt.bar(x_vals, y_vals)
        plt.title("Neuron-Level Tarantula Scores: 'faulty_output'")
        plt.xlabel("Neuron Index in 'faulty_output' layer")
        plt.ylabel("Suspiciousness Score")
        plt.tight_layout()
        plt.savefig("neuron_scores_faulty_output.png")
        plt.close()
    else:
        no_data_line = "No neuron-level data for 'faulty_output'."
        print(no_data_line)
        results_lines.append(no_data_line)
        


for layer_name in tracked_layers:
    # We only plot if we have coverage for that layer
    if layer_name not in layer_avg_coverage:
        continue

    # Convert to floats explicitly (safe-guard)
    pass_cov = [
        float(c) for c, outcome in zip(layer_avg_coverage[layer_name], test_outcomes)
        if not outcome
    ]
    fail_cov = [
        float(c) for c, outcome in zip(layer_avg_coverage[layer_name], test_outcomes)
        if outcome
    ]

    if len(pass_cov) == 0 and len(fail_cov) == 0:
        # no data
        continue
    
    print(f"Layer: {layer_name}")
    print(f"  Pass Runs: {pass_cov}")
    print(f"  Fail Runs: {fail_cov}")
    results_lines.append(f"Layer: {layer_name}")
    results_lines.append(f"  Pass Runs: {pass_cov}")
    results_lines.append(f"  Fail Runs: {fail_cov}")

    # Use a list of two arrays => boxplot will interpret them as [pass, fail]
    data_for_boxplot = [pass_cov, fail_cov]
    plt.figure(figsize=(6, 4))
    sns.boxplot(data=data_for_boxplot, width=0.4)
    plt.xticks([0, 1], ["Pass Runs", "Fail Runs"])
    plt.ylabel("Avg Coverage")
    plt.title(f"Distribution of avg coverage for layer: {layer_name}")
    plt.tight_layout()
    plt.savefig(f"coverage_{layer_name}.png")
    plt.close()
    
    
with open("neuron_scores.pkl", "wb") as f:
    pickle.dump(neuron_scores, f)
print("neuron_scores.pkl saved successfully.")   
    
with open("results_output2.txt", "w") as f:
    for line in results_lines:
        f.write(line + "\n")
        

def print_layer_info(model):
    """
    Print the number of neurons/filters in each layer
    """
    print("\nLayer Information:")
    for layer in model.layers:
        if isinstance(layer, (layers.Conv2D, layers.Dense)):
            if isinstance(layer, layers.Conv2D):
                print(f"{layer.name}: {layer.filters} filters")
            else:
                print(f"{layer.name}: {layer.units} neurons")

# Add this after model creation to see the information
model = create_model()
print_layer_info(model)
        
