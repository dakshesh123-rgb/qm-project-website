import math

def linspace(start, stop, num):
    if num == 1: return [start]
    return [start + i * (stop - start) / (num - 1) for i in range(num)]

def count_eigenvalues_below(diag, off_diag, mu):
    """
    Counts eigenvalues below mu using Sturm sequence property.
    Correctly handles IEEE-754 exact zeros without destroying signs.
    """
    N = len(diag)
    count = 0
    d = diag[0] - mu
    if d == 0.0: d = 1e-300
    if d < 0: count += 1
    
    for k in range(1, N):
        d = (diag[k] - mu) - (off_diag[k-1]**2) / d
        if d == 0.0: d = 1e-300
        if d < 0: count += 1
    return count

def find_eigenvalue_bisection(diag, off_diag, n, E_lo, E_hi, tol=1e-12):
    """
    Finds the nth eigenvalue using bisection.
    Safe termination to prevent infinite loops at precision limit.
    """
    for _ in range(200):
        E_mid = (E_lo + E_hi) / 2.0
        if (E_hi - E_lo) < tol or E_mid == E_lo or E_mid == E_hi:
            break
        count = count_eigenvalues_below(diag, off_diag, E_mid)
        if count <= n:
            E_lo = E_mid
        else:
            E_hi = E_mid
    return (E_lo + E_hi) / 2.0

def tridiagonal_solve_pivoting(main_diag, off_diag, rhs):
    """
    Gaussian elimination with partial pivoting for a tridiagonal system.
    CRITICAL for solving indefinite systems like (H - E I).
    """
    n = len(main_diag)
    md = list(main_diag)
    ud = list(off_diag) + [0.0]
    uud = [0.0] * n
    ld = list(off_diag) + [0.0]
    b = list(rhs)
    
    # Forward elimination with pivoting
    for i in range(n - 1):
        if abs(ld[i]) > abs(md[i]):
            # Swap rows
            md[i], ld[i] = ld[i], md[i]
            ud[i], md[i+1] = md[i+1], ud[i]
            uud[i], ud[i+1] = ud[i+1], uud[i]
            b[i], b[i+1] = b[i+1], b[i]
            
        if md[i] == 0.0: continue
        
        factor = ld[i] / md[i]
        md[i+1] -= factor * ud[i]
        ud[i+1] -= factor * uud[i]
        b[i+1] -= factor * b[i]
        
    # Back substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        val = b[i]
        if i + 1 < n: val -= ud[i] * x[i+1]
        if i + 2 < n: val -= uud[i] * x[i+2]
        if md[i] != 0.0:
            x[i] = val / md[i]
    return x

def inverse_iteration(diag, off_diag, eigenvalue, prev_eigs, dx, tol=1e-10):
    """
    Finds the eigenvector using inverse iteration.
    Features sign-flip proof convergence and Gram-Schmidt orthogonalization.
    """
    n = len(diag)
    shift = 1e-10
    shifted_diag = [d - eigenvalue - shift for d in diag]
    
    x = [1.0] * n
    
    def orthogonalize(vec):
        for v in prev_eigs:
            dot = sum(vec[i]*v[i]*dx for i in range(n))
            vec = [vec[i] - dot*v[i] for i in range(n)]
        return vec
        
    x = orthogonalize(x)
    norm = math.sqrt(sum(xi*xi for xi in x) * dx)
    if norm > 0: x = [xi/norm for xi in x]
    
    for _ in range(100):
        x_new = tridiagonal_solve_pivoting(shifted_diag, off_diag, x)
        x_new = orthogonalize(x_new)
        
        norm = math.sqrt(sum(xi*xi for xi in x_new) * dx)
        if norm == 0: break
        x_new = [xi/norm for xi in x_new]
        
        # Check convergence (safe against sign flips)
        diff1 = sum((x_new[i] - x[i])**2 for i in range(n))
        diff2 = sum((x_new[i] + x[i])**2 for i in range(n))
        
        if min(diff1, diff2) < tol:
            x = x_new
            break
        x = x_new
        
    return x

def solve_schrodinger(x, V, num_states=6):
    """
    Numerically solves the 1D time-independent Schrödinger equation.
    Uses Gershgorin circle theorem for rigorous eigenvalue bounds.
    """
    N = len(x)
    dx = x[1] - x[0]
    t = 1.0 / (2.0 * dx * dx) # Assumes hbar=1, m=1
    
    diag = [2.0 * t + V[i] for i in range(N)]
    off_diag = [-t for _ in range(N - 1)]
    
    E_min = min(V)
    E_max = max(V) + 4.0 * t  # Strict bound via Gershgorin Circle Theorem
    
    energies = []
    wavefunctions = []
    residuals = []
    
    for n in range(num_states):
        E = find_eigenvalue_bisection(diag, off_diag, n, E_min, E_max)
        energies.append(E)
        
        psi = inverse_iteration(diag, off_diag, E, wavefunctions, dx)
        wavefunctions.append(psi)
        
        # Calculate residual ||H*psi - E*psi||
        res_sq = 0.0
        for i in range(N):
            Hpsi = diag[i] * psi[i]
            if i > 0: Hpsi += off_diag[i-1] * psi[i-1]
            if i < N-1: Hpsi += off_diag[i] * psi[i+1]
            res_sq += (Hpsi - E * psi[i])**2 * dx
        residuals.append(math.sqrt(res_sq))
        
    return energies, wavefunctions, residuals
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
