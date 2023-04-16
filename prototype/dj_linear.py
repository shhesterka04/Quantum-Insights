from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram

def dj_oracle_linear(n, f):
    oracle = QuantumCircuit(n+1)

    for i in range(n):
        oracle.cx(i, n)

    U_f = oracle.to_gate()
    U_f.name = "U_f"
    return U_f

def extended_deutsch_josza(n, f):
    dj_circuit = QuantumCircuit(n+1, n)

    for i in range(n):
        dj_circuit.h(i)

    dj_circuit.x(n)
    dj_circuit.h(n)

    oracle = dj_oracle_linear(n, f)
    dj_circuit.append(oracle, range(n+1))

    for i in range(n):
        dj_circuit.h(i)

    for i in range(n):
        dj_circuit.measure(i, i)

    return dj_circuit

def run_algorithm(circuit):
    simulator = Aer.get_backend('qasm_simulator')
    t_qc = transpile(circuit, simulator)
    qobj = assemble(t_qc)
    result = simulator.run(qobj).result()
    return result.get_counts()

n = 3
f = lambda x: x[0] ^ x[1] ^ x[2] # Example linear function
circuit = extended_deutsch_josza(n, f)
result = run_algorithm(circuit)
plot_histogram(result)
