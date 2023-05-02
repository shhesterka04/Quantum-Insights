import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram

def monotonicity_oracle(qc, n, monotonic=True):
    if monotonic:
        for i in range(n-1):
            qc.cx(i, n+i)
            qc.x(n+i)
        qc.barrier()
        qc.mct(list(range(n, 2*n-1)), 2*n-1)
        qc.barrier()
        for i in range(n-1):
            qc.x(n+i) 
            qc.cx(i, n+i)
    else:
        # An example of a non-monotonic function using a CNOT gate
        qc.cx(0, 1)

def deutsch_josza_monotonicity(n, monotonic=True):
    qc = QuantumCircuit(2*n, n)
    
    qc.x(2*n-1)
    qc.h(range(2*n))
    
    monotonicity_oracle(qc, n, monotonic)
    
    qc.h(range(n))
    qc.measure(range(n), range(n))
    
    aer_sim = Aer.get_backend('aer_simulator')
    shots = 1024
    qobj = assemble(qc, shots=shots)
    result = aer_sim.run(qobj).result()
    counts = result.get_counts(qc)
    
    return plot_histogram(counts)

# Test with a monotonically increasing function
deutsch_josza_monotonicity(3, monotonic=True).show()

# Test with a non-monotonic function
deutsch_josza_monotonicity(3, monotonic=False).show()
