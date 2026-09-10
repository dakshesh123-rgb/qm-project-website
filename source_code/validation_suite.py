import math
from robust_qm_solver import solve_schrodinger, linspace

def test_infinite_square_well():
    print("==================================================")
    print(" BENCHMARK 1: INFINITE SQUARE WELL CONVERGENCE")
    print("==================================================")
    L = 1.0
    print(f"{'N':>5} | {'E_0 Num':>12} | {'E_0 Exact':>12} | {'Error':>12} | {'Residual L2':>12}")
    print("-" * 60)
    for N in [100, 200, 400, 800]:
        x = linspace(0, L, N+2)[1:-1]
        V = [0.0]*N
        energies, _, res = solve_schrodinger(x, V, num_states=1)
        exact = (math.pi**2) / 2.0
        err = abs(energies[0] - exact)
        print(f"{N:5d} | {energies[0]:12.6f} | {exact:12.6f} | {err:12.2e} | {res[0]:12.2e}")
    print("Notice that Error drops by a factor of 4 as N doubles (O(dx^2) convergence).\n")

def test_morse():
    print("==================================================")
    print(" BENCHMARK 2: MORSE POTENTIAL (ANALYTICAL MATCH)")
    print("==================================================")
    # Use a large domain to avoid boundary truncation!
    N = 1000
    x = linspace(-5, 15, N)
    D = 10.0; a = 1.0
    V = [D * (1 - math.exp(-a*xi))**2 for xi in x]
    
    print("Solving for 4 lowest bound states...")
    energies, _, res = solve_schrodinger(x, V, num_states=4)
    
    omega = a * math.sqrt(2*D) # m=1
    print(f"{'State':>5} | {'E_n Num':>12} | {'E_n Exact':>12} | {'Error':>12} | {'Residual L2':>12}")
    print("-" * 60)
    for n in range(4):
        exact = omega*(n + 0.5) - (omega**2 / (4*D)) * (n + 0.5)**2
        err = abs(energies[n] - exact)
        print(f"{n:5d} | {energies[n]:12.6f} | {exact:12.6f} | {err:12.2e} | {res[n]:12.2e}")

if __name__ == "__main__":
    test_infinite_square_well()
    test_morse()
