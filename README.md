# 🔔 HelloBell

> A quantum computing "hello world" — creating a **Bell state** with Qiskit.

[![Qiskit](https://img.shields.io/badge/Qiskit-2.x-6929C4?logo=ibm)](https://qiskit.org)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://python.org)

**HelloBell** is the quantum analogue of printing `"hello, world"`. It builds the simplest entangled state in quantum computing — the [Bell state](https://en.wikipedia.org/wiki/Bell_state)

$$|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

using a Hadamard gate followed by a CNOT gate, then verifies entanglement via:

- **Expectation values** — $\langle ZZ \rangle = 1$, $\langle XX \rangle = 1$, $\langle ZI \rangle = \langle IZ \rangle = 0$
- **Measurement sampling** — a 50/50 split between $|00\rangle$ and $|11\rangle$

---

## 🚀 Getting Started

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run the hello world
python hello_bell.py
```

Expected output:

```
Expectation values (ideal Bell state):
  ⟨ZZ⟩ = 1.0000   (should be  1.0000)
  ⟨ZI⟩ = 0.0000   (should be  0.0000)
  ⟨IZ⟩ = 0.0000   (should be  0.0000)
  ⟨XX⟩ = 1.0000   (should be  1.0000)

Measurement counts (1024 shots):
  |00⟩:  542  (52.9%)
  |11⟩:  482  (47.1%)
```

## 📁 Project Structure

```
HelloBell/
├── hello_bell.py      # Bell-state circuit + verification
├── .venv/             # Python virtual environment
├── .gitignore
└── README.md
```

## 🔬 What's Happening?

| Gate | Qubit 0 | Qubit 1 | Effect |
|------|---------|---------|--------|
| H    | `─┤H├─` | `─────` | Creates superposition: $|0\rangle \to \frac{|0\rangle + |1\rangle}{\sqrt{2}}$ |
| CX   | `─■───` | `─┤X├─` | CNOT flips q₁ when q₀ = $|1\rangle$, producing $\frac{|00\rangle + |11\rangle}{\sqrt{2}}$ |

The result is a **maximally entangled** two-qubit state — measuring one qubit instantly tells you the outcome of the other.

## 📦 Requirements

- Python 3.12+
- [Qiskit](https://pypi.org/project/qiskit/) 2.x (installed in `.venv/`)

## 📄 License

This project is for educational purposes. Feel free to use, share, and modify.
