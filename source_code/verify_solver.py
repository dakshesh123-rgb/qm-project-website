"""
=============================================================================
VERIFICATION SCRIPT — Infinite Square Well & Harmonic Oscillator
=============================================================================

This script verifies our Schrödinger equation solver by comparing
numerical results against known analytical solutions.

If our numerical energies and wave functions match the textbook answers,
we know the solver is working correctly!

This is CRITICAL for any computational physics paper — you MUST verify
your code against known solutions before using it on new problems.

Author: [Your Name]
Date: September 2026
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for saving figures

# Import our modules
from solver import solve_schrodinger, probability_density
from potentials import (
    infinite_square_well, infinite_well_analytical_energies,
    infinite_well_analytical_wavefunction,
    harmonic_oscillator, harmonic_analytical_energies
)


def verify_infinite_well():
    """
    Verify the solver against the infinite square well.

    Known solution:
        E_n = n²π² / (2L²)
        ψ_n(x) = √(2/L) · sin(nπx/L)
    """
    print("=" * 70)
    print("VERIFICATION 1: Infinite Square Well (Particle in a Box)")
    print("=" * 70)

    # --- Setup ---
    L = 1.0          # Well width
    N = 500          # Number of grid points (more = more accurate)
    num_states = 6   # Number of states to compute

    # Create spatial grid (a bit wider than the well for boundary conditions)
    x = np.linspace(-0.5, L + 0.5, N)

    # Define the potential
    V = infinite_square_well(x, L=L)

    # --- Solve ---
    energies, wavefunctions, _ = solve_schrodinger(x, V, num_states=num_states)

    # --- Compare with analytical solution ---
    analytical_E = infinite_well_analytical_energies(num_states, L=L)

    print(f"\n{'State n':>8} {'Numerical E':>15} {'Analytical E':>15} {'Error (%)':>12}")
    print("-" * 55)
    for i in range(num_states):
        error = abs(energies[i] - analytical_E[i]) / analytical_E[i] * 100
        print(f"{i+1:>8d} {energies[i]:>15.6f} {analytical_E[i]:>15.6f} {error:>11.6f}%")

    # --- Plot ---
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Plot 1: Potential + Energy Levels
    ax = axes[0]
    ax.fill_between(x, 0, np.clip(V, 0, max(analytical_E) * 1.5),
                    alpha=0.15, color='gray', label='Potential V(x)')
    for i in range(num_states):
        ax.axhline(y=energies[i], color=f'C{i}', linestyle='--', alpha=0.7)
        ax.axhline(y=analytical_E[i], color=f'C{i}', linestyle=':', alpha=0.4)
    ax.set_xlim(-0.2, L + 0.2)
    ax.set_ylim(0, analytical_E[-1] * 1.3)
    ax.set_xlabel('Position x', fontsize=12)
    ax.set_ylabel('Energy', fontsize=12)
    ax.set_title('Energy Levels\n(dashed=numerical, dotted=analytical)', fontsize=12)
    ax.legend(fontsize=10)

    # Plot 2: Wave Functions
    ax = axes[1]
    for i in range(min(4, num_states)):
        # Scale wave functions for display and offset by energy
        psi_scaled = wavefunctions[:, i] * 3 + energies[i]
        ax.plot(x, psi_scaled, color=f'C{i}', linewidth=1.5,
                label=f'n={i+1}, E={energies[i]:.2f}')
        ax.axhline(y=energies[i], color=f'C{i}', linestyle=':', alpha=0.3)

    # Draw well walls
    ax.axvline(x=0, color='black', linewidth=2)
    ax.axvline(x=L, color='black', linewidth=2)
    ax.set_xlim(-0.2, L + 0.2)
    ax.set_xlabel('Position x', fontsize=12)
    ax.set_ylabel('ψ(x) + E_n (offset)', fontsize=12)
    ax.set_title('Wave Functions ψ_n(x)', fontsize=12)
    ax.legend(fontsize=9, loc='upper right')

    # Plot 3: Numerical vs Analytical Wave Functions
    ax = axes[2]
    for i in range(min(3, num_states)):
        # Analytical wave function
        psi_analytical = infinite_well_analytical_wavefunction(x, i + 1, L)

        # Find the well region for comparison
        mask = (x > 0) & (x < L)

        ax.plot(x[mask], wavefunctions[mask, i], '-', color=f'C{i}',
                linewidth=2, label=f'Numerical n={i+1}')
        ax.plot(x[mask], np.abs(psi_analytical[mask]), '--', color=f'C{i}',
                linewidth=2, alpha=0.5, label=f'Analytical n={i+1}')

    ax.set_xlabel('Position x', fontsize=12)
    ax.set_ylabel('ψ(x)', fontsize=12)
    ax.set_title('Numerical vs Analytical\n(solid=numerical, dashed=analytical)', fontsize=12)
    ax.legend(fontsize=9)

    plt.suptitle('VERIFICATION: Infinite Square Well', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('verification_infinite_well.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n✅ Figure saved: verification_infinite_well.png")


def verify_harmonic_oscillator():
    """
    Verify the solver against the quantum harmonic oscillator.

    Known solution:
        E_n = ω(n + ½)    for n = 0, 1, 2, ...
    """
    print("\n" + "=" * 70)
    print("VERIFICATION 2: Quantum Harmonic Oscillator")
    print("=" * 70)

    # --- Setup ---
    omega = 1.0        # Angular frequency
    N = 800            # More points needed (wave function extends further)
    num_states = 8

    # Grid needs to be wide enough for the wave function to decay
    x = np.linspace(-8, 8, N)

    # Define the potential
    V = harmonic_oscillator(x, omega=omega)

    # --- Solve ---
    energies, wavefunctions, _ = solve_schrodinger(x, V, num_states=num_states)

    # --- Compare ---
    analytical_E = harmonic_analytical_energies(num_states, omega=omega)

    print(f"\n{'State n':>8} {'Numerical E':>15} {'Analytical E':>15} {'Error (%)':>12}")
    print("-" * 55)
    for i in range(num_states):
        error = abs(energies[i] - analytical_E[i]) / analytical_E[i] * 100
        print(f"{i:>8d} {energies[i]:>15.6f} {analytical_E[i]:>15.6f} {error:>11.6f}%")

    # --- Plot ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Wave functions in the potential
    ax = axes[0]
    ax.plot(x, V, 'k-', linewidth=2, label='V(x) = ½ω²x²')
    ax.fill_between(x, 0, V, alpha=0.05, color='gray')

    for i in range(min(5, num_states)):
        psi_scaled = wavefunctions[:, i] * 1.5 + energies[i]
        ax.plot(x, psi_scaled, color=f'C{i}', linewidth=1.5)
        ax.axhline(y=energies[i], color=f'C{i}', linestyle=':', alpha=0.3)
        ax.text(5, energies[i], f'n={i}', fontsize=9, color=f'C{i}',
                verticalalignment='center')

    ax.set_xlim(-6, 7)
    ax.set_ylim(-0.5, energies[min(5, num_states)-1] + 2)
    ax.set_xlabel('Position x', fontsize=12)
    ax.set_ylabel('Energy / ψ(x)', fontsize=12)
    ax.set_title('Wave Functions in Harmonic Potential', fontsize=12)

    # Plot 2: Probability densities
    ax = axes[1]
    for i in range(min(5, num_states)):
        prob = probability_density(wavefunctions[:, i])
        prob_scaled = prob * 2 + energies[i]
        ax.fill_between(x, energies[i], prob_scaled, alpha=0.3, color=f'C{i}')
        ax.plot(x, prob_scaled, color=f'C{i}', linewidth=1.5,
                label=f'n={i}, E={energies[i]:.3f}')
        ax.axhline(y=energies[i], color=f'C{i}', linestyle=':', alpha=0.3)

    ax.plot(x, V, 'k-', linewidth=2, alpha=0.5)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-0.5, energies[min(5, num_states)-1] + 2)
    ax.set_xlabel('Position x', fontsize=12)
    ax.set_ylabel('Energy / |ψ(x)|²', fontsize=12)
    ax.set_title('Probability Densities |ψ_n(x)|²', fontsize=12)
    ax.legend(fontsize=9, loc='upper right')

    plt.suptitle('VERIFICATION: Quantum Harmonic Oscillator', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('verification_harmonic_oscillator.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n✅ Figure saved: verification_harmonic_oscillator.png")


def verify_energy_scaling():
    """
    Additional verification: Check that E_n ∝ n² for the infinite well.
    This is a fundamental property — if our solver gets this right,
    it's definitely working.
    """
    print("\n" + "=" * 70)
    print("VERIFICATION 3: Energy Scaling (E_n ∝ n²)")
    print("=" * 70)

    L = 1.0
    N = 500
    num_states = 15

    x = np.linspace(-0.5, L + 0.5, N)
    V = infinite_square_well(x, L=L)
    energies, _ = solve_schrodinger(x, V, num_states=num_states)

    # E_n should be proportional to n²
    n_values = np.arange(1, num_states + 1)
    E1 = energies[0]  # Ground state energy

    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.scatter(n_values**2, energies, color='blue', s=50, zorder=5,
               label='Numerical: $E_n$')
    ax.plot(n_values**2, E1 * n_values**2, 'r--', linewidth=2,
            label=f'Theoretical: $E_1 \\cdot n^2$')

    ax.set_xlabel('$n^2$', fontsize=14)
    ax.set_ylabel('Energy $E_n$', fontsize=14)
    ax.set_title('Energy Scaling Verification: $E_n = E_1 \\cdot n^2$', fontsize=14)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('verification_energy_scaling.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n✅ Figure saved: verification_energy_scaling.png")
    print(f"\nE_n / (E_1 · n²) ratios (should all be ≈ 1.0):")
    for i, n in enumerate(n_values):
        ratio = energies[i] / (E1 * n**2)
        print(f"  n={n:2d}: {ratio:.6f}")


# =============================================================================
# RUN ALL VERIFICATIONS
# =============================================================================
if __name__ == "__main__":
    print("\n🔬 QUANTUM MECHANICS SOLVER — VERIFICATION SUITE\n")

    verify_infinite_well()
    verify_harmonic_oscillator()
    verify_energy_scaling()

    print("\n" + "=" * 70)
    print("✅ ALL VERIFICATIONS COMPLETE")
    print("=" * 70)
    print("\nCheck the generated PNG files for visual verification!")
    print("If the numerical and analytical results match closely,")
    print("our solver is working correctly and ready for research! 🚀\n")
