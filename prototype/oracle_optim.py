import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram

def search_oracle(qc, address_qubits, target_qubits, target_value):
    # Example oracle that marks the target_value in the list of integers
    for idx, value in enumerate(target_value):
        if value == '0':
            qc.x(target_qubits[idx])

    qc.mct(target_qubits, address_qubits[-1], address_qubits[:-1], mode='basic') 
    
    for idx, value in enumerate(target_value):
        if value == '0':
            qc.x(target_qubits[idx])

def grover_diffusion(qc, address_qubits):
    qc.h(address_qubits)
    qc.x(address_qubits)
    qc.h(address_qubits[-1])
    qc.mct(address_qubits[:-1], address_qubits[-1], mode='basic')
    qc.h(address_qubits[-1])
    qc.x(address_qubits)
    qc.h(address_qubits)

def grover_search(target_value):
    n_address_qubits = int(np.ceil(np.log2(len(target_value))))
    n_target_qubits = len(target_value)

    qc = QuantumCircuit(n_address_qubits + n_target_qubits, n_address_qubits)

    qc.h(range(n_address_qubits))
    qc.barrier()

    iterations = int(np.sqrt(2**n_address_qubits))
    for _ in range(iterations):
        search_oracle(qc, range(n_address_qubits), range(n_address_qubits, n_address_qubits + n_target_qubits), target_value)
        qc.barrier()
        grover_diffusion(qc, range(n_address_qubits))
        qc.barrier()

    qc.measure(range(n_address_qubits), range(n_address_qubits))

    aer_sim = Aer.get_backend('aer_simulator')
    shots = 1024
    qobj = assemble(qc, shots=shots)
    result = aer_sim.run(qobj).result()
    counts = result.get_counts(qc)

    return plot_histogram(counts)

target_value = '110'
grover_search(target_value).show()
