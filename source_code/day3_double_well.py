from verify_pure_python import solve_schrodinger, double_well_potential, linspace
import math

def run_splitting_study():
    print("=================================================================")
    print(" DAY 3: SYSTEMATIC DOUBLE WELL TUNNEL SPLITTING STUDY")
    print("=================================================================")
    print(" Simulating an Ammonia-like molecule (Chapter 16).")
    print(" We will increase the central barrier (V0) and measure")
    print(" how the tunnel splitting (ΔE) shrinks exponentially.")
    print("-----------------------------------------------------------------")
    
    # High resolution grid for accurate eigenvalues
    N = 2000
    x = linspace(-5.0, 5.0, N)
    a = 1.5  # Fixed distance between the wells
    
    print(f" Grid points: {N}")
    print(f" Well separation parameter 'a': {a}")
    print("-----------------------------------------------------------------")
    print("  V0   |    E0    |    E1    |      ΔE     | ln(ΔE)")
    print("-----------------------------------------------------------------")
    
    results = []
    
    # Sweep barrier height from 3.0 to 14.0
    v0_values = [3.0 + i*1.0 for i in range(13)]
    
    for V0 in v0_values:
        V = double_well_potential(x, V0=V0, a=a)
        
        # We only need the first 2 states (ground and 1st excited)
        energies, _ = solve_schrodinger(x, V, num_states=2)
        E0 = energies[0]
        E1 = energies[1]
        
        dE = E1 - E0
        
        # Prevent math domain error if splitting hits 0 due to precision
        if dE > 1e-12:
            ln_dE = math.log(dE)
        else:
            ln_dE = float('-inf')
            
        results.append((V0, dE))
        print(f" {V0:4.1f} | {E0:8.5f} | {E1:8.5f} | {dE:11.7f} | {ln_dE:7.3f}")

    print("=================================================================")
    print(" Notice how ln(ΔE) decreases almost linearly as V0 increases.")
    print(" This confirms that tunneling splitting decays exponentially")
    print(" as the barrier gets higher!")
    print("=================================================================")

if __name__ == "__main__":
    run_splitting_study()
