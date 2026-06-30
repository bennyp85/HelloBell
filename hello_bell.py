"""
HelloBell — A quantum computing "hello world".

Explores all four Bell states — the simplest examples of quantum entanglement.
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator, StatevectorSampler
from qiskit.quantum_info import SparsePauliOp

estimator = StatevectorEstimator()
sampler = StatevectorSampler()


def run_and_print(name, qc):
    """Build circuit with measurements, print it, then show expectation values
    and measurement counts."""
    qc_meas = qc.copy()
    qc_meas.measure_all()

    print("=" * 52)
    print(f"  {name}")
    print("=" * 52)
    print()
    print(qc_meas.draw("text"))
    print()

    # Expectation values
    obs = [SparsePauliOp("ZZ"), SparsePauliOp("XX")]
    job = estimator.run([(qc, obs)])
    ev = job.result()[0].data.evs
    print(f"  <ZZ> = {ev[0]:+.4f}")
    print(f"  <XX> = {ev[1]:+.4f}")
    print()

    # Measurement counts
    job = sampler.run([qc_meas], shots=1024)
    counts = job.result()[0].data.meas.get_counts()
    print(f"  Measurement counts (1024 shots):")
    for bits in sorted(counts):
        pct = 100 * counts[bits] / 1024
        print(f"    |{bits}>: {counts[bits]:>4}  ({pct:.1f}%)")
    print()


# ── Bell state 1: |Phi+> = (|00> + |11>) / sqrt(2) ───────────────
# Recipe: H on q0, then CNOT with q0 as control and q1 as target.
# Result: q0 and q1 are always in the SAME state → CORRELATED.

def phi_plus():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


# ── Bell state 2: |Phi-> = (|00> - |11>) / sqrt(2) ───────────────
# Recipe: H, CNOT, then Z on q0.
# Z flips the phase of |1>, turning |11> into -|11>.
# Result: same as Phi+ but with a phase difference → still CORRELATED.

def phi_minus():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.z(0)
    return qc


# ── Bell state 3: |Psi+> = (|01> + |10>) / sqrt(2) ───────────────
# Recipe: H, CNOT, then X on q0.
# X flips q0 from |0> to |1> and vice versa, swapping the basis states.
# Result: q0 and q1 are always in OPPOSITE states → ANTI-CORRELATED.

def psi_plus():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(0)
    return qc


# ── Bell state 4: |Psi-> = (|01> - |10>) / sqrt(2) ───────────────
# Recipe: H, CNOT, X on q0, then Z on q0.
# X swaps, Z adds a phase flip.
# Result: same as Psi+ but with a phase difference → still ANTI-CORRELATED.

def psi_minus():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(0)
    qc.z(0)
    return qc


# ── Run them all ──────────────────────────────────────────────────

run_and_print("Phi+  (CORRELATED -- same bits)", phi_plus())
run_and_print("Phi-  (CORRELATED -- same bits)", phi_minus())
run_and_print("Psi+  (ANTI-CORRELATED -- opposite bits)", psi_plus())
run_and_print("Psi-  (ANTI-CORRELATED -- opposite bits)", psi_minus())
