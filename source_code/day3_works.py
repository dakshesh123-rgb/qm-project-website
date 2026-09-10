import sys
import math
sys.path.insert(0, '/root/qm_project')
from verify_pure_python import solve_schrodinger, linspace, ascii_plot, double_well_potential, morse_potential

def do_double_well_study():
    print("=" * 66)
    print(" TASK 1: DOUBLE WELL TUNNEL SPLITTING STUDY (Fine Resolution)")
    print("=" * 66)
    N = 1000 
    x = linspace(-6, 6, N)
    
    a_values = [1.0, 1.2, 1.5, 1.8, 2.0, 2.2, 2.5]
    V0 = 10.0
    
    print(f"Sweeping well separation 'a' at constant barrier height V0={V0}:")
    print(f"{'a':>5} | {'E0':>12} | {'E1':>12} | {'Splitting (E1-E0)':>18}")
    print("-" * 55)
    
    with open("/root/qm_project/day3_double_well_splitting.txt", "w") as f:
        f.write("a, E0, E1, Splitting\n")
        for a in a_values:
            V = double_well_potential(x, V0=V0, a=a)
            energies, _ = solve_schrodinger(x, V, num_states=2)
            E0, E1 = energies[0], energies[1]
            splitting = E1 - E0
            print(f"{a:5.1f} | {E0:12.6f} | {E1:12.6f} | {splitting:18.8f}")
            f.write(f"{a},{E0},{E1},{splitting}\n")
    print("Saved results to day3_double_well_splitting.txt\n")

def do_morse_potential_study():
    print("=" * 66)
    print(" TASK 2: MORSE POTENTIAL STUDY (Molecular Vibrations)")
    print("=" * 66)
    N = 800
    x = linspace(-2, 8, N)
    
    D = 15.0 
    a = 1.0  
    
    V = morse_potential(x, D=D, a=a, x0=0.0)
    
    ascii_plot(x, V, width=55, height=10, title="Morse Potential V(x)")
    
    num_states = 5
    energies, wavefunctions, _ = solve_schrodinger(x, V, num_states)
    
    print("\nEnergy Levels in Morse Potential:")
    with open("/root/qm_project/day3_morse_energies.txt", "w") as f:
        f.write("n, Energy\n")
        for i, E in enumerate(energies):
            print(f"n={i}: E = {E:.6f}")
            f.write(f"{i},{E}\n")
    
    if len(energies) >= 2:
        print(f"Spacing E1-E0 = {energies[1] - energies[0]:.6f}")
        print(f"Spacing E2-E1 = {energies[2] - energies[1]:.6f}")
        print(f"Spacing E3-E2 = {energies[3] - energies[2]:.6f}")
        
    print("\nPlotting wavefunctions:")
    for n in range(min(3, num_states)):
        ascii_plot(x, wavefunctions[n], width=55, height=12,
                   title=f"ψ_{n}(x) Morse State | E = {energies[n]:.4f}", zero_line=True)
    print("Saved energy results to day3_morse_energies.txt\n")

if __name__ == "__main__":
    do_double_well_study()
    do_morse_potential_study()
    print("Day 3 tasks completed successfully!")
