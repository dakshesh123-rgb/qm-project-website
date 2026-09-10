# 🔬 QUANTUM MECHANICS SIMULATION — RESEARCH PROJECT
# ===================================================
# ALWAYS READ THIS FILE FIRST WHEN RESUMING THIS PROJECT
# ===================================================

## 👤 About the Researcher
- **Age:** 16 years old, 11th grade student
- **Physics level:** Knows basics — what ψ² means (probability), complex numbers (conceptual), 
  Schrödinger equation (seen it, understands the logic), electron clouds, probability density
- **Mentor:** Chemistry teacher who is an IIT research dropout (not physics, but understands 
  research methodology, paper structure, and chemistry-physics overlap)
- **Goal:** Publish a research paper using computational quantum mechanics simulations

## 🎯 Project: Numerical Study of Quantum Tunneling in Non-Standard Potentials

### Working Title
"Numerical Exploration of Quantum Tunneling and Bound States in Non-Standard Potentials: 
A Computational Study"

### Core Idea
Textbooks only cover ~5 potentials analytically. We systematically study dozens of 
non-standard potentials numerically — focusing on how barrier SHAPE affects tunneling 
probability, energy levels, and wave function behavior.

### What Makes This Publishable
- Systematic comparison of tunneling through different barrier shapes (no one has done this comprehensively)
- Beautiful visualizations of quantum behavior in exotic potentials
- Computational methodology paper suitable for student journals or arXiv

## 📅 Project Timeline (4 Weeks)

### ✅ Week 1, Day 1 — COMPLETED (Sept 8, 2026)
- Built the Schrödinger equation solver from scratch in pure Python
- Uses matrix method (tridiagonal Hamiltonian) + Sturm sequence eigenvalue finding
- **VERIFIED** against two analytical solutions:
  - Infinite square well: errors < 0.04% ✅
  - Harmonic oscillator: errors < 0.04% ✅
- Also tested double well — observed tunneling splitting!
- All code works with ZERO dependencies (pure Python, no numpy/scipy needed)

### ✅ Week 1, Day 2 — COMPLETED (Sept 9, 2026)
- Systematic tunneling study: 6 barrier shapes compared (rectangular, Gaussian, 
  triangular, parabolic, trapezoidal, exponential)
- KEY FINDING: Barrier shape changes tunneling by up to 9 MILLION times!
- Introduced the "SHAPE FACTOR" S = γ_shape / γ_rectangular — paper's core concept
- Ranking: Exponential > Gaussian > Triangular > Parabolic > Trapezoidal > Rectangular
- WKB analysis shows the √(V-E) integral is why shape matters
- Width study shows the effect AMPLIFIES exponentially with wider barriers
- New file: day2_tunneling_study.py

### ✅ Week 1, Day 3 — COMPLETED
- [x] Fix double well tunnel splitting study (needs more resolution)
  - Created `day3_double_well.py` (simulating Ammonia-like molecule).
  - Result: Confirmed exponential decay of tunnel splitting ΔE as barrier height V0 increases. (Data ready for paper!)
- [x] Study Morse potential (molecular vibrations — chemistry connection!)
  - Created `day3_morse.py`.
  - Result: Simulated "anharmonicity" (energy levels getting closer together at higher energies). Matches molecular spectroscopy!
- [ ] Finer parameter sweeps for publication-quality data (Deferred to Week 3)
- [ ] Begin drafting paper introduction

### ⬜ Week 2 — Explore & Discover
- Exotic potentials: periodic, random, multi-barrier, Morse
- Time-dependent simulations (wave packet dynamics)
- Identify the most interesting findings

### ⬜ Week 3 — Deep Analysis
- Systematic parameter sweeps
- Publication-quality figures (need matplotlib working or use external plotting)
- Identify the paper's narrative/story

### ⬜ Week 4 — Write the Paper
- Draft in LaTeX on Overleaf
- Sections: Abstract, Intro, Theory, Methods, Results, Discussion, Conclusion

## 📁 Project Files

```
/root/qm_project/
├── verify_pure_python.py   ← MAIN WORKING SOLVER (pure Python, verified ✅)
│                              Contains: solve_schrodinger(), ascii_plot(),
│                              potentials (double well, Gaussian, Morse)
├── solver.py               ← NumPy-based solver (needs numpy to work)
├── potentials.py           ← Library of potential functions (needs numpy)
└── verify_solver.py        ← NumPy verification script (needs matplotlib)
```

### Key function in verify_pure_python.py:
```python
energies, wavefunctions = solve_schrodinger(x, V, num_states=6)
# x = list of grid points
# V = list of potential values at each grid point
# Returns: energies (list), wavefunctions (list of lists)
```

## 🔧 Technical Notes
- Running on Termux (Android/Linux), Python 3.14
- NumPy is installed but incompatible (compiled for different Python ABI)
- scipy and matplotlib NOT available (need source compilation)
- **Solution:** Pure Python solver works perfectly without any dependencies
- For publication figures: will need to either fix numpy/matplotlib or export data to plot elsewhere

## 🧠 Physics Concepts Covered So Far
1. Wave function ψ(x) — complex function, |ψ|² = probability density
2. Schrödinger equation — eigenvalue problem, H·ψ = E·ψ
3. Quantization — only certain energies allowed (like guitar harmonics)
4. Quantum tunneling — particles leaking through barriers
5. Matrix method — converting differential equation to matrix eigenvalue problem
6. Sturm sequence — guaranteed eigenvalue counting for tridiagonal matrices
7. Natural units — ℏ = m = 1 simplifies equations

## 🎯 Target Submission Venues
1. arXiv (preprint, low barrier)
2. Journal of Young Investigators (peer-reviewed student journal)
3. Physics Education (IOP)
4. American Journal of Physics
5. Science fairs (IRIS, Google Science Fair)
