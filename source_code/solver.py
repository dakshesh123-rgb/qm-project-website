"""
=============================================================================
QUANTUM MECHANICS SIMULATION — CORE SOLVER
=============================================================================

This module solves the 1D Time-Independent Schrödinger Equation (TISE):

    -ℏ²/(2m) · d²ψ/dx² + V(x)·ψ(x) = E·ψ(x)

In plain English:
    The total energy (E) of a quantum particle equals its kinetic energy
    (related to how fast the wave function curves) plus its potential energy V(x).

HOW IT WORKS (The Matrix Method):
    1. We can't solve this equation analytically for most potentials V(x)
    2. So we DISCRETIZE space: instead of continuous x, we use N grid points
    3. The second derivative d²ψ/dx² becomes a matrix operation (finite differences)
    4. The whole equation becomes a matrix eigenvalue problem: H·ψ = E·ψ
    5. NumPy finds ALL the eigenvalues (energies) and eigenvectors (wave functions) at once!

We use NATURAL UNITS: ℏ = 1, m = 1
    This simplifies the math without losing any physics.
    We can always convert back to SI units later.

Author: [Your Name]
Date: September 2026
=============================================================================
"""

import numpy as np
from numpy import linalg


def build_hamiltonian(x, V):
    """
    Build the Hamiltonian matrix H = T + V for a 1D system.

    The Hamiltonian is the total energy operator. It has two parts:
        T = Kinetic energy (how fast the particle moves)
        V = Potential energy (the "landscape" the particle lives in)

    Parameters
    ----------
    x : numpy array
        The spatial grid points (positions where we evaluate the wave function)
    V : numpy array
        The potential energy at each grid point V(x)

    Returns
    -------
    H : 2D numpy array (matrix)
        The Hamiltonian matrix of size (N x N) where N = len(x)
    """
    N = len(x)
    dx = x[1] - x[0]  # Grid spacing

    # === KINETIC ENERGY MATRIX (T) ===
    # The second derivative d²ψ/dx² is approximated by finite differences:
    #   d²ψ/dx² ≈ (ψ[i+1] - 2·ψ[i] + ψ[i-1]) / dx²
    #
    # This gives us a TRIDIAGONAL matrix:
    #   Main diagonal:  -2/dx²  (multiplied by -ℏ²/2m = -1/2 in natural units)
    #   Off-diagonals:  +1/dx²  (multiplied by -ℏ²/2m = -1/2 in natural units)
    #
    # So T = (-1/2) * tridiagonal matrix

    # Build the tridiagonal matrix for d²/dx²
    main_diag = -2.0 * np.ones(N) / dx**2
    off_diag = 1.0 * np.ones(N - 1) / dx**2

    # Kinetic energy: T = -ℏ²/(2m) · d²/dx² = -0.5 · d²/dx² (in natural units)
    T = -0.5 * (np.diag(main_diag) + np.diag(off_diag, 1) + np.diag(off_diag, -1))

    # === POTENTIAL ENERGY MATRIX (V) ===
    # V is simply a diagonal matrix: V(x) at each grid point
    V_matrix = np.diag(V)

    # === HAMILTONIAN ===
    # H = T + V (total energy = kinetic + potential)
    H = T + V_matrix

    return H


def solve_schrodinger(x, V, num_states=10):
    """
    Solve the 1D Time-Independent Schrödinger Equation.

    Given a potential V(x), find the allowed energies and wave functions.

    Parameters
    ----------
    x : numpy array
        Spatial grid points
    V : numpy array
        Potential energy at each grid point
    num_states : int
        Number of lowest energy states to return

    Returns
    -------
    energies : numpy array
        The allowed energy eigenvalues (sorted from lowest to highest)
    wavefunctions : 2D numpy array
        Each column wavefunctions[:, i] is the wave function for energy energies[i]
        Wave functions are normalized so that ∫|ψ|² dx = 1
    """
    # Step 1: Build the Hamiltonian matrix
    H = build_hamiltonian(x, V)

    # Step 2: Solve the eigenvalue problem H·ψ = E·ψ
    # eigh = eigenvalue solver for Hermitian (symmetric) matrices
    # It returns ALL eigenvalues and eigenvectors, sorted by energy
    eigenvalues, eigenvectors = linalg.eigh(H)

    # Step 3: Keep only the lowest 'num_states' states
    energies = eigenvalues[:num_states]
    wavefunctions = eigenvectors[:, :num_states]

    # Step 4: Normalize the wave functions
    # The probability of finding the particle SOMEWHERE must be 1:
    #   ∫|ψ(x)|² dx = 1
    dx = x[1] - x[0]
    for i in range(num_states):
        norm = np.sqrt(np.trapezoid(wavefunctions[:, i]**2, x))
        wavefunctions[:, i] /= norm

        # Convention: make the wave function positive at its first major peak
        # (this is just for consistent plotting — physics doesn't change)
        if wavefunctions[np.argmax(np.abs(wavefunctions[:, i])), i] < 0:
            wavefunctions[:, i] *= -1

    return energies, wavefunctions


def probability_density(psi):
    """
    Calculate the probability density |ψ(x)|².

    In quantum mechanics, |ψ(x)|² tells you the PROBABILITY of finding
    the particle at position x. This is the physical observable — not ψ itself.

    Parameters
    ----------
    psi : numpy array
        The wave function ψ(x)

    Returns
    -------
    numpy array
        The probability density |ψ(x)|²
    """
    return np.abs(psi)**2


def expectation_value(x, psi, operator_values):
    """
    Calculate the expectation value <ψ|O|ψ> = ∫ ψ*(x) · O(x) · ψ(x) dx

    The expectation value is the AVERAGE value you'd measure if you
    repeated the measurement many times on identically prepared systems.

    Parameters
    ----------
    x : numpy array
        Spatial grid points
    psi : numpy array
        The wave function
    operator_values : numpy array
        The operator O evaluated at each grid point
        (for position: operator_values = x, for potential: operator_values = V)

    Returns
    -------
    float
        The expectation value
    """
    integrand = np.conj(psi) * operator_values * psi
    return np.real(np.trapezoid(integrand, x))


def tunneling_probability(x, psi, barrier_start, barrier_end):
    """
    Calculate the probability of finding the particle INSIDE or BEYOND a barrier.

    This is quantum tunneling — classically impossible, but quantum mechanics
    allows particles to "leak through" energy barriers!

    Parameters
    ----------
    x : numpy array
        Spatial grid points
    psi : numpy array
        The wave function
    barrier_start : float
        Left edge of the barrier
    barrier_end : float
        Right edge of the barrier

    Returns
    -------
    float
        Probability of finding the particle beyond the barrier (tunneling probability)
    """
    # Find indices beyond the barrier
    beyond_barrier = x >= barrier_end
    prob_density = probability_density(psi)

    # Integrate |ψ|² beyond the barrier
    if np.any(beyond_barrier):
        return np.trapezoid(prob_density[beyond_barrier], x[beyond_barrier])
    return 0.0
