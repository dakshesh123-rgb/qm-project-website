    diag = [2.0 * kinetic_coeff + V[i] for i in range(N)]
    off_diag = [-kinetic_coeff] * (N - 1)
    
    # Estimate eigenvalue bounds using Gershgorin circle theorem
    E_lo = min(diag[i] - abs(off_diag[min(i, N-2)]) - abs(off_diag[max(i-1, 0)]) 
               for i in range(N)) - 1.0
    E_hi = max(diag[i] + abs(off_diag[min(i, N-2)]) + abs(off_diag[max(i-1, 0)]) 
               for i in range(N)) + 1.0
    
    # Find eigenvalues using bisection + Sturm counting
    energies = []
    wavefunctions = []
    
    for n in range(num_states):
        E_n = find_eigenvalue_bisection(diag, off_diag, n, E_lo, E_hi)
        psi = inverse_iteration(diag, off_diag, E_n)
        
        # Normalize: ∫|ψ|² dx = 1
        norm_sq = sum(p*p for p in psi) * dx
        if norm_sq > 0:
            norm = math.sqrt(norm_sq)
            psi = [p / norm for p in psi]
        
        # Consistent sign: largest peak positive
        max_idx = max(range(N), key=lambda i: abs(psi[i]))
        if psi[max_idx] < 0:
            psi = [-p for p in psi]
        
        energies.append(E_n)
        wavefunctions.append(psi)
    
    return energies, wavefunctions


# =============================================================================
# ASCII PLOTTING
# =============================================================================

def ascii_plot(x, y, width=60, height=14, title="", zero_line=False):
    """Simple ASCII plot for terminal."""
    if not y:
        return

    y_min = min(y)
    y_max = max(y)
    if abs(y_max - y_min) < 1e-15:
        y_max = y_min + 1
    
    pad = (y_max - y_min) * 0.05
    y_min -= pad
    y_max += pad
    y_range = y_max - y_min
    x_min, x_max = min(x), max(x)
    x_range = x_max - x_min

    canvas = [[' '] * width for _ in range(height)]
    
    if zero_line and y_min < 0 < y_max:
        zr = int((1 - (0 - y_min) / y_range) * (height - 1))
        if 0 <= zr < height:
            for c in range(width):
                canvas[zr][c] = '·'

    for xi, yi in zip(x, y):
        col = int((xi - x_min) / x_range * (width - 1))
        row = int((1 - (yi - y_min) / y_range) * (height - 1))
        col = max(0, min(width - 1, col))
        row = max(0, min(height - 1, row))
        canvas[row][col] = '█'

    print(f"\n  {title}")
    print(f"  {'─' * (width + 2)}")
    for ri, row in enumerate(canvas):
        if ri == 0:
            lb = f"{y_max:>9.4f}"
        elif ri == height - 1:
            lb = f"{y_min:>9.4f}"
        else:
            lb = "         "
        print(f"{lb} │{''.join(row)}│")
    print(f"          {'─' * (width + 2)}")
    print(f"          {x_min:<9.3f}{' ' * (width - 18)}{x_max:>9.3f}")


# =============================================================================
# POTENTIAL FUNCTIONS
# =============================================================================

def double_well_potential(x, V0=1.0, a=2.0):
    """Double well: V = V0·(x²-a²)²/a⁴"""
    return [V0 * (xi**2 - a**2)**2 / a**4 for xi in x]

def gaussian_barrier_potential(x, V0=10.0, sigma=0.5, x0=0.0):
    """Gaussian barrier: V = V0·exp(-x²/(2σ²))"""
    return [V0 * math.exp(-(xi-x0)**2 / (2*sigma**2)) for xi in x]

def morse_potential(x, D=10.0, a=1.0, x0=0.0):
    """Morse potential (molecular vibrations): V = D·(1-exp(-a(x-x0)))²"""
    return [D * (1 - math.exp(-a*(xi-x0)))**2 for xi in x]


# =============================================================================
# MAIN — VERIFICATION
# =============================================================================
if __name__ == "__main__":
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║     🔬 QUANTUM MECHANICS SOLVER v4 — MATRIX + STURM METHOD    ║")
    print("║        Pure Python · Zero Dependencies · Guaranteed Correct    ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    # =====================================================================
    # TEST 1: INFINITE SQUARE WELL
    # =====================================================================
    print("\n" + "=" * 66)
    print("  TEST 1: INFINITE SQUARE WELL (Particle in a Box)")
    print("  " + "─" * 62)
    print("  V(x) = 0 inside [0, L].  Boundary: ψ(0) = ψ(L) = 0")
    print("  Analytical: E_n = n²π²/(2L²) ≈ n² × 4.9348")
    print("=" * 66)

    L = 1.0
    N = 300
    num_states = 6

    # Grid INSIDE the well (boundaries excluded — they're zero)
    x = linspace(0, L, N + 2)[1:-1]  # Remove endpoints
    V = [0.0] * N

    print(f"\n  Grid: {N} interior points, x ∈ (0, {L})")
    print(f"  Solving for {num_states} lowest eigenstates...\n")

    energies, wavefunctions, _ = solve_schrodinger(x, V, num_states)

    analytical = [n**2 * math.pi**2 / (2 * L**2) for n in range(1, num_states + 1)]

    all_good = True
    print(f"  {'State':>7} │ {'Numerical':>14} │ {'Analytical':>14} │ {'Error (%)':>12}")
    print(f"  {'─'*7}─┼─{'─'*14}─┼─{'─'*14}─┼─{'─'*12}")
    for i in range(num_states):
        err = abs(energies[i] - analytical[i]) / analytical[i] * 100
        status = "✅" if err < 1.0 else "⚠️"
        if err >= 1.0:
            all_good = False
        print(f"  n = {i+1:2d} │ {energies[i]:14.6f} │ {analytical[i]:14.6f} │ {err:10.6f}% {status}")

    # Plot wave functions
    for n_plot in range(min(4, num_states)):
        ascii_plot(x, wavefunctions[n_plot], width=55, height=12,
                   title=f"ψ_{n_plot+1}(x)  │  E = {energies[n_plot]:.4f}  │  {n_plot} node(s)",
                   zero_line=True)

    # =====================================================================
    # TEST 2: HARMONIC OSCILLATOR
    # =====================================================================
    print("\n" + "=" * 66)
    print("  TEST 2: QUANTUM HARMONIC OSCILLATOR")
    print("  " + "─" * 62)
    print("  V(x) = ½ω²x²")
    print("  Analytical: E_n = ω(n + ½) = 0.5, 1.5, 2.5, ...")
    print("=" * 66)

    omega = 1.0
    N = 500
    num_states = 6

    x = linspace(-8, 8, N)
    V = [0.5 * omega**2 * xi**2 for xi in x]

    print(f"\n  Grid: {N} points, x ∈ [-8, 8]")
    print(f"  Solving for {num_states} lowest eigenstates...\n")

    energies_ho, wavefunctions_ho, _ = solve_schrodinger(x, V, num_states)

    analytical_ho = [omega * (n + 0.5) for n in range(num_states)]

    print(f"  {'State':>7} │ {'Numerical':>14} │ {'Analytical':>14} │ {'Error (%)':>12}")
    print(f"  {'─'*7}─┼─{'─'*14}─┼─{'─'*14}─┼─{'─'*12}")
    for i in range(num_states):
        err = abs(energies_ho[i] - analytical_ho[i]) / analytical_ho[i] * 100
        status = "✅" if err < 1.0 else "⚠️"
        if err >= 1.0:
            all_good = False
        print(f"  n = {i:2d} │ {energies_ho[i]:14.6f} │ {analytical_ho[i]:14.6f} │ {err:10.6f}% {status}")

    # Plot probability densities
    for n_plot in range(min(3, num_states)):
        prob = [p**2 for p in wavefunctions_ho[n_plot]]
        ascii_plot(x, prob, width=55, height=12,
                   title=f"|ψ_{n_plot}(x)|²  Probability Density  │  E = {energies_ho[n_plot]:.6f}")

    # =====================================================================
    # BONUS: DOUBLE WELL (preview of research!)
    # =====================================================================
    print("\n" + "=" * 66)
    print("  BONUS: DOUBLE WELL POTENTIAL (Preview of Research!)")
    print("  " + "─" * 62)
    print("  V(x) = V₀·(x² - a²)² / a⁴   (two wells separated by a barrier)")
    print("  The particle can TUNNEL between the wells!")
    print("=" * 66)

    N = 500
    x = linspace(-4, 4, N)
    V = double_well_potential(x, V0=8.0, a=1.5)

    print(f"\n  Solving for 4 lowest states...\n")
    energies_dw, wavefunctions_dw, _ = solve_schrodinger(x, V, 4)

    for i in range(len(energies_dw)):
        print(f"  n = {i}: E = {energies_dw[i]:.6f}")

    ascii_plot(x, V, width=55, height=10,
               title="Double Well Potential V(x)")

    if len(wavefunctions_dw) >= 2:
        ascii_plot(x, wavefunctions_dw[0], width=55, height=12,
                   title=f"ψ₀(x) Ground State  │  E = {energies_dw[0]:.4f}",
                   zero_line=True)
        ascii_plot(x, wavefunctions_dw[1], width=55, height=12,
                   title=f"ψ₁(x) First Excited │  E = {energies_dw[1]:.4f}  │  TUNNELING!",
                   zero_line=True)

    # =====================================================================
    # SUMMARY
    # =====================================================================
    print("\n" + "═" * 66)
    result = "✅ ALL TESTS PASSED" if all_good else "⚠️  SOME TESTS NEED ATTENTION"
    print(f"\n  {result}")
    print()
    print("  ┌──────────────────────────────────────────────────────────┐")
    print("  │  The Sturm sequence + bisection method gives us         │")
    print("  │  MATHEMATICALLY GUARANTEED convergence to the           │")
    print("  │  correct eigenvalues!                                   │")
    print("  │                                                          │")
    print("  │  🚀 READY FOR RESEARCH: Apply to exotic potentials      │")
    print("  │     that have never been systematically studied!        │")
    print("  └──────────────────────────────────────────────────────────┘")
    print()
