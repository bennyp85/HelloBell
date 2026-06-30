"""
HelloBell — A quantum computing "hello world".

Explores all four Bell states (the maximally entangled two-qubit basis):
  |Phi+>  = (|00> + |11>) / sqrt(2)    -- correlated      (ZZ = +1)
  |Phi->  = (|00> - |11>) / sqrt(2)    -- correlated      (ZZ = +1)
  |Psi+>  = (|01> + |10>) / sqrt(2)    -- ANTI-correlated (ZZ = -1)
  |Psi->  = (|01> - |10>) / sqrt(2)    -- ANTI-correlated (ZZ = -1)
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator, StatevectorSampler
from qiskit.quantum_info import SparsePauliOp

estimator = StatevectorEstimator()
sampler = StatevectorSampler()
observables = [SparsePauliOp("ZZ"), SparsePauliOp("ZI"),
               SparsePauliOp("IZ"), SparsePauliOp("XX")]


def bell_state_circuit(gate0, gate1):
    """Return (no-measure, with-measure) for a Bell state.
    Start |00>, apply H then CX then optional gate0/gate1 on q0.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    if gate0:
        getattr(qc, gate0)(0)
    if gate1:
        getattr(qc, gate1)(0)
    qc_m = qc.copy()
    qc_m.measure_all()
    return qc, qc_m


def analyze(name, short, qc, qc_m):
    """Print circuit, expectation values, and measurement counts."""
    print("=" * 52)
    print(f"  HelloBell -- {name}")
    print("=" * 52)
    print()
    print(qc_m.draw("text"))
    print()

    # Expectation values
    job = estimator.run([(qc, observables)])
    ev = job.result()[0].data.evs
    labels = ["ZZ", "ZI", "IZ", "XX"]
    expected = {"Phi+": [1, 0, 0, 1], "Phi-": [1, 0, 0, -1],
                "Psi+": [-1, 0, 0, 1], "Psi-": [-1, 0, 0, -1]}
    print("Expectation values:")
    for lab, val, exp in zip(labels, ev, expected[short]):
        mark = "OK" if abs(val - exp) < 1e-6 else "MISMATCH"
        print(f"  <{lab}> = {val:+.4f}  (expected {exp:+.4f})  [{mark}]")
    print()

    # Measurement counts
    job = sampler.run([qc_m], shots=1024)
    counts = job.result()[0].data.meas.get_counts()
    print("Measurement counts (1024 shots):")
    for bits in sorted(counts):
        pct = 100 * counts[bits] / 1024
        print(f"  |{bits}>: {counts[bits]:>4}  ({pct:.1f}%)")
    print()


# ── All four Bell states ──────────────────────────────────────────

# |Phi+>  = (|00> + |11>) / sqrt(2)   -- H + CX             -- CORRELATED
qc_p, qc_pm = bell_state_circuit(None, None)
analyze("Phi+  (correlated)", "Phi+", qc_p, qc_pm)

# |Phi->  = (|00> - |11>) / sqrt(2)   -- H + CX + Z(q0)     -- CORRELATED
qc_f, qc_fm = bell_state_circuit("z", None)
analyze("Phi-  (correlated)", "Phi-", qc_f, qc_fm)

# |Psi+>  = (|01> + |10>) / sqrt(2)   -- H + CX + X(q0)     -- ANTI-correlated
qc_pp, qc_ppm = bell_state_circuit("x", None)
analyze("Psi+  (ANTI-correlated)", "Psi+", qc_pp, qc_ppm)

# |Psi->  = (|01> - |10>) / sqrt(2)   -- H + CX + X(q0) + Z(q0) -- ANTI-correlated
qc_pm, qc_pmm = bell_state_circuit("x", "z")
analyze("Psi-  (ANTI-correlated)", "Psi-", qc_pm, qc_pmm)
