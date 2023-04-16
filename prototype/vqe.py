from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit import Parameter
from qiskit.opflow import Z, X, I
from qiskit.opflow.state_fns import CircuitStateFn
from qiskit.algorithms.optimizers import COBYLA
import numpy as np

# Define the Hamiltonian
H = 0.5 * (Z ^ Z) - 0.5 * (I ^ X)

# Define the ansatz circuit
theta = Parameter('θ')
ansatz = QuantumCircuit(2)
ansatz.h(0)
ansatz.rx(theta, 1)
ansatz.cx(0, 1)

# Create the expectation value objective function
ansatz_state = CircuitStateFn(ansatz)
expectation_value = (ansatz_state.adjoint() @ H @ ansatz_state).reduce()

# Define the VQE optimization problem
def vqe_objective(params):
    bound_circuit = ansatz.bind_parameters(params)
    result = execute(bound_circuit, Aer.get_backend('statevector_simulator')).result()
    statevector = result.get_statevector()
    return np.real(expectation_value.eval().subs(ansatz_state.parameter_expression, statevector))

# Optimize the ansatz parameters using a classical optimizer
optimizer = COBYLA(maxiter=500, tol=1e-6)
result = optimizer.optimize(num_vars=1, objective_function=vqe_objective, initial_point=np.random.rand(1))

# Print the optimized parameters and the estimated ground state energy
print("Optimized parameters:", result[0])
print("Estimated ground state energy:", result[1])
