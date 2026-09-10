"""
=============================================================================
POTENTIAL ENERGY FUNCTIONS
=============================================================================

This module defines various potential energy functions V(x).

The potential is the "landscape" that the quantum particle lives in.
Think of it like a hill-and-valley terrain — the particle's behavior
is entirely determined by the shape of this landscape.

TEXTBOOK POTENTIALS (well-studied, used for verification):
    - Infinite square well
    - Finite square well
    - Harmonic oscillator
    - Step potential

NON-STANDARD POTENTIALS (our research focus!):
    - Asymmetric double well
    - Gaussian barrier
    - Triangular barrier
    - Multiple barriers
    - Smooth periodic potential
    - And more to come...

Author: [Your Name]
Date: September 2026
=============================================================================
"""

import numpy as np


# =============================================================================
# TEXTBOOK POTENTIALS (for verification)
# =============================================================================

def infinite_square_well(x, L=1.0):
    """
    Infinite square well (particle in a box).

    V(x) = 0     for 0 < x < L
    V(x) = ∞     otherwise

    The simplest quantum system! The particle is trapped in a box.
    We approximate ∞ by making the walls very high (1e10).

    ANALYTICAL SOLUTION (to verify our code):
        E_n = n²π²ℏ² / (2mL²) = n²π² / (2L²)  [natural units]
        ψ_n(x) = √(2/L) · sin(nπx/L)

    Parameters
    ----------
    x : numpy array
        Spatial grid points
    L : float
        Width of the well
    """
    V = np.zeros_like(x)
    V[x <= 0] = 1e10
    V[x >= L] = 1e10
    return V


def infinite_well_analytical_energies(n_max, L=1.0):
    """
    Analytical energy levels for the infinite square well.

    E_n = n²π² / (2L²)  for n = 1, 2, 3, ...

    Parameters
    ----------
    n_max : int
        Number of energy levels to compute
    L : float
        Width of the well
    """
    n = np.arange(1, n_max + 1)
    return n**2 * np.pi**2 / (2 * L**2)


def infinite_well_analytical_wavefunction(x, n, L=1.0):
    """
    Analytical wave function for the infinite square well.

    ψ_n(x) = √(2/L) · sin(nπx/L)

    Parameters
    ----------
    x : numpy array
        Spatial grid points
    n : int
        Quantum number (1, 2, 3, ...)
    L : float
        Width of the well
    """
    psi = np.sqrt(2.0 / L) * np.sin(n * np.pi * x / L)
    # Set to zero outside the well
    psi[x <= 0] = 0
    psi[x >= L] = 0
    return psi


def finite_square_well(x, V0=50.0, L=1.0):
    """
    Finite square well.

    V(x) = -V0   for |x| < L/2
    V(x) = 0     otherwise

    Unlike the infinite well, particles CAN leak out!
    The wave function extends beyond the well walls (tunneling!).

    Parameters
    ----------
    x : numpy array
    V0 : float
        Depth of the well (positive number)
    L : float
        Width of the well
    """
    V = np.zeros_like(x)
    V[np.abs(x) < L / 2] = -V0
    return V


def harmonic_oscillator(x, omega=1.0):
    """
    Quantum Harmonic Oscillator.

    V(x) = ½mω²x² = ½ω²x²  [natural units, m=1]

    A particle in a parabolic potential (like a mass on a spring).
    One of the most important systems in all of physics!

    ANALYTICAL SOLUTION:
        E_n = ℏω(n + ½) = ω(n + ½)  [natural units]
        for n = 0, 1, 2, ...

    Parameters
    ----------
    x : numpy array
    omega : float
        Angular frequency of the oscillator
    """
    return 0.5 * omega**2 * x**2


def harmonic_analytical_energies(n_max, omega=1.0):
    """
    Analytical energy levels for the harmonic oscillator.

    E_n = ω(n + ½)  for n = 0, 1, 2, ...
    """
    n = np.arange(0, n_max)
    return omega * (n + 0.5)


# =============================================================================
# NON-STANDARD POTENTIALS (research targets!)
# =============================================================================

def double_well(x, V0=20.0, a=1.0, b=0.5):
    """
    Symmetric double well potential.

    Two wells separated by a barrier. A particle can tunnel between them!
    This is the basis of many real phenomena: ammonia molecule, quantum computing, etc.

    Parameters
    ----------
    x : numpy array
    V0 : float
        Controls the height and shape
    a : float
        Distance between wells
    b : float
        Width parameter
    """
    return V0 * (x**2 - a**2)**2 / a**4


def asymmetric_double_well(x, V0=20.0, a=1.0, tilt=2.0):
    """
    Asymmetric double well — one well is deeper than the other.

    This is MORE realistic than the symmetric version (perfect symmetry
    almost never occurs in nature). How does asymmetry affect tunneling?

    Parameters
    ----------
    x : numpy array
    V0 : float
        Overall scale
    a : float
        Distance between wells
    tilt : float
        How much one well is deeper than the other
    """
    return V0 * (x**2 - a**2)**2 / a**4 + tilt * x


def gaussian_barrier(x, V0=10.0, sigma=0.5, x0=0.0):
    """
    Gaussian-shaped barrier.

    V(x) = V0 · exp(-(x - x0)² / (2σ²))

    Smoother than a rectangular barrier. How does the smooth shape
    affect tunneling compared to a sharp rectangular barrier?

    Parameters
    ----------
    x : numpy array
    V0 : float
        Height of the barrier
    sigma : float
        Width of the barrier
    x0 : float
        Center of the barrier
    """
    return V0 * np.exp(-(x - x0)**2 / (2 * sigma**2))


def rectangular_barrier(x, V0=10.0, width=1.0, x0=0.0):
    """
    Rectangular (step) barrier.

    The classic textbook barrier for tunneling problems.

    Parameters
    ----------
    x : numpy array
    V0 : float
        Height of the barrier
    width : float
        Width of the barrier
    x0 : float
        Center of the barrier
    """
    V = np.zeros_like(x)
    V[(x > x0 - width/2) & (x < x0 + width/2)] = V0
    return V


def triangular_barrier(x, V0=10.0, width=2.0, x0=0.0):
    """
    Triangular barrier — linear slopes on both sides.

    How does a sharp peak vs. a flat top affect tunneling?

    Parameters
    ----------
    x : numpy array
    V0 : float
        Height of the barrier
    width : float
        Base width of the triangle
    x0 : float
        Center of the barrier
    """
    V = np.zeros_like(x)
    left = (x >= x0 - width/2) & (x <= x0)
    right = (x > x0) & (x <= x0 + width/2)
    V[left] = V0 * (1 + 2*(x[left] - x0) / width)
    V[right] = V0 * (1 - 2*(x[right] - x0) / width)
    return V


def multi_barrier(x, n_barriers=3, V0=10.0, width=0.5, spacing=2.0):
    """
    Multiple evenly-spaced barriers.

    This creates a simple model of a crystal lattice!
    Interesting quantum effects emerge: resonant tunneling, band structure.

    Parameters
    ----------
    x : numpy array
    n_barriers : int
        Number of barriers
    V0 : float
        Height of each barrier
    width : float
        Width of each barrier
    spacing : float
        Distance between barrier centers
    """
    V = np.zeros_like(x)
    total_width = (n_barriers - 1) * spacing
    start = -total_width / 2

    for i in range(n_barriers):
        center = start + i * spacing
        V += rectangular_barrier(x, V0=V0, width=width, x0=center)

    return V


def smooth_periodic(x, V0=10.0, period=2.0):
    """
    Smooth periodic potential (cosine).

    V(x) = V0 · [1 - cos(2πx/a)] / 2

    A smooth version of the Kronig-Penney model.
    This is how electrons behave in a crystal!

    Parameters
    ----------
    x : numpy array
    V0 : float
        Amplitude of the potential
    period : float
        Spatial period
    """
    return V0 * (1 - np.cos(2 * np.pi * x / period)) / 2


def morse_potential(x, D=10.0, a=1.0, x0=0.0):
    """
    Morse potential — realistic model of a diatomic molecule.

    V(x) = D · (1 - exp(-a(x - x0)))²

    Unlike the harmonic oscillator, this has a finite depth,
    so only a finite number of bound states exist!

    Your chemistry teacher will love this one — it models
    molecular vibrations much better than the harmonic oscillator.

    Parameters
    ----------
    x : numpy array
    D : float
        Depth of the well (dissociation energy)
    a : float
        Controls the width of the well
    x0 : float
        Equilibrium position
    """
    return D * (1 - np.exp(-a * (x - x0)))**2


def woods_saxon(x, V0=50.0, R=2.0, a=0.5):
    """
    Woods-Saxon potential — used in nuclear physics.

    V(x) = -V0 / (1 + exp((|x| - R) / a))

    Models the potential felt by a nucleon inside a nucleus.

    Parameters
    ----------
    x : numpy array
    V0 : float
        Depth of the potential
    R : float
        Nuclear radius
    a : float
        Surface thickness (diffuseness)
    """
    return -V0 / (1 + np.exp((np.abs(x) - R) / a))
