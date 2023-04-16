import numpy as np
from qiskit import Aer
from qiskit.circuit.library import ZZFeatureMap
from qiskit.utils import QuantumInstance
from qiskit_machine_learning.algorithms import QSVM
from qiskit_machine_learning.datasets import ad_hoc_data
from qiskit_machine_learning.datasets.dataset_helper import dataset_to_data_and_labels

# Load the ad hoc dataset
training_dataset, test_dataset, datapoints, class_labels = ad_hoc_data(
    training_size=20, test_size=10, n=2, gap=0.3, plot_data=False
)

# Set up the feature map and the QSVM algorithm
feature_map = ZZFeatureMap(feature_dimension=2, reps=2, entanglement="linear")
backend = Aer.get_backend("aer_simulator_statevector")
quantum_instance = QuantumInstance(backend, shots=1024, seed_simulator=42, seed_transpiler=42)

qsvm = QSVM(feature_map, training_dataset, test_dataset, None, quantum_instance)

# Train the QSVM algorithm
qsvm_result = qsvm.run(quantum_instance)

# Test the QSVM algorithm
predicted_labels = qsvm.predict(datapoints[0])

# Calculate the accuracy
correct_labels = np.sum(predicted_labels == datapoints[1])
accuracy = correct_labels / len(datapoints[1])
print("QSVM Classification Accuracy: {:.2f}".format(accuracy))
