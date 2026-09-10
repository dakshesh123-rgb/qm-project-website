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
