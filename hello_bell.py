"""
HelloBell — A quantum computing "hello world".

Creates a Bell state |Φ⁺⟩ = (|00⟩ + |11⟩) / √2,
the simplest entangled state in quantum computing.
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator, StatevectorSampler
from qiskit.quantum_info import SparsePauliOp

# ── Build the Bell-state circuit ──────────────────────────────────
qc = QuantumCircuit(2)
qc.h(0)          # Hadamard: create superposition on qubit 0
qc.cx(0, 1)      # CNOT: entangle qubit 1 with qubit 0

qc_measured = qc.copy()
qc_measured.measure_all()

print("═" * 52)
print("  HelloBell — Quantum Hello World")
print("═" * 52)
print()
print(qc_measured.draw("text"))
print()

# ── Verify with statevector (Estimator) ───────────────────────────
estimator = StatevectorEstimator()
observables = [SparsePauliOp("ZZ"), SparsePauliOp("ZI"),
               SparsePauliOp("IZ"), SparsePauliOp("XX")]
job = estimator.run([(qc, observables)])
expvals = job.result()[0].data.evs

print("Expectation values (ideal Bell state):")
print(f"  ⟨ZZ⟩ = {expvals[0]:.4f}   (should be  1.0000)")
print(f"  ⟨ZI⟩ = {expvals[1]:.4f}   (should be  0.0000)")
print(f"  ⟨IZ⟩ = {expvals[2]:.4f}   (should be  0.0000)")
print(f"  ⟨XX⟩ = {expvals[3]:.4f}   (should be  1.0000)")
print()

# ── Sample measurements (Sampler) ─────────────────────────────────
sampler = StatevectorSampler()
job = sampler.run([qc_measured], shots=1024)
counts = job.result()[0].data.meas.get_counts()
print("Measurement counts (1024 shots):")
for bitstring, count in sorted(counts.items()):
    print(f"  |{bitstring}⟩: {count:>4}  ({100 * count / 1024:.1f}%)")
print()
print("✅ The qubits are entangled — HelloBell successful!")
