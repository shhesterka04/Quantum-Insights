import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram


def example_periodic_function(x):
    return (x % 3) + 1

def periodicity_oracle(qc, x_qubits, p_qubits, ancilla_qubits):
    # Custom oracle implementation for the example periodic function
    for i in range(len(x_qubits)):
        qc.cx(x_qubits[i], ancilla_qubits[i])
        qc.cx(p_qubits[i], ancilla_qubits[i])
        qc.barrier()

def inverse_qft(circuit, qubits):
    """Apply the inverse Quantum Fourier Transform on the given qubits."""
    num_qubits = len(qubits)
    for j in range(num_qubits):
        for m in range(j):
            circuit.cu1(-np.pi / float(2**(j - m)), qubits[j], qubits[m])
        circuit.h(qubits[j])

def periodicity_detection(n):
    x_qubits = list(range(n))
    p_qubits = list(range(n, 2*n))
    ancilla_qubits = list(range(2*n, 3*n-1))

    qc = QuantumCircuit(3*n-1, n)
    
    qc.h(x_qubits)
    qc.h(p_qubits)
    qc.barrier()

    periodicity_oracle(qc, x_qubits, p_qubits, ancilla_qubits)
    qc.barrier()

    inverse_qft(qc, p_qubits)
    qc.measure(p_qubits, range(n))

    aer_sim = Aer.get_backend('aer_simulator')
    shots = 1024
    qobj = assemble(qc, shots=shots)
    result = aer_sim.run(qobj).result()
    counts = result.get_counts(qc)

    return plot_histogram(counts)

n = 3
periodicity_detection(n).show()
