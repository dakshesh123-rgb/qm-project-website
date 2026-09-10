from verify_pure_python import solve_schrodinger, morse_potential, linspace, ascii_plot
import math

def run_morse_study():
    print("=================================================================")
    print(" DAY 3: MORSE POTENTIAL STUDY (MOLECULAR VIBRATIONS)")
    print("=================================================================")
    print(" Simulating the chemical bond of a diatomic molecule (e.g., HCl).")
    print(" Unlike a simple spring (Harmonic Oscillator), real chemical bonds")
    print(" can BREAK if you pull them too hard. This is why the Morse")
    print(" potential levels off at a dissociation energy D.")
    print("-----------------------------------------------------------------")
    
    N = 1000
    # The Morse potential is steep on the left (atoms repelling)
    # and shallow on the right (atoms breaking apart)
    x = linspace(-2.0, 10.0, N)
    
    # Parameters for the molecule
    D = 15.0   # Dissociation energy (how hard to break the bond)
    a = 0.5    # Width parameter of the well
    x0 = 0.0   # Equilibrium bond length (shifted to 0 for simplicity)
    
    V = morse_potential(x, D=D, a=a, x0=x0)
    
    print(f" Dissociation Energy (D): {D}")
    print(f" Solving for lowest 6 vibrational states...")
    
    energies, wavefunctions, _ = solve_schrodinger(x, V, num_states=6)
    
    print("-----------------------------------------------------------------")
    print(" State (n) | Energy (E_n) | Spacing (E_n - E_{n-1})")
    print("-----------------------------------------------------------------")
    
    for i in range(len(energies)):
        E = energies[i]
        if i == 0:
            spacing = "   N/A   "
        else:
            spacing = f"{E - energies[i-1]:.6f}"
            
        print(f"    {i}      |   {E:8.5f}   |   {spacing}")

    print("=================================================================")
    print(" THE PHYSICS DISCOVERY:")
    print(" In a standard Harmonic Oscillator, the energy spacing is CONSTANT.")
    print(" But look at the Spacing column here! The energy levels get")
    print(" CLOSER TOGETHER as you go higher. This is called 'Anharmonicity'")
    print(" and perfectly matches experimental spectroscopy of molecules!")
    print("=================================================================")
    
    # Plot the potential and the 4th excited state to show it leaking to the right
    ascii_plot(x, V, width=60, height=12, title="Morse Potential V(x) - Asymmetric Chemical Bond")
    ascii_plot(x, wavefunctions[0], width=60, height=10, title="ψ_0 (Ground State) - mostly centered", zero_line=True)
    ascii_plot(x, wavefunctions[4], width=60, height=10, title="ψ_4 (Highly Excited) - 'leaning' towards dissociation", zero_line=True)

if __name__ == "__main__":
    run_morse_study()
