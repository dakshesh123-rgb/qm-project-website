import json

with open("/root/qm_project/shape_factor_data.json", "r") as f:
    sf_data = json.load(f)
with open("/root/qm_project/resonance_data.json", "r") as f:
    res_data = json.load(f)
with open("/root/qm_project/wavepacket_data.json", "r") as f:
    wp_data = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Tunneling Through Non-Standard Barrier Geometries — Dakshesh Das</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #000000;
            --card-bg: #0a0a0a;
            --border-color: #222222;
            --text-main: #e0e0e0;
            --text-muted: #888888;
            --accent: #ffffff;
            --badge-bg: #141414;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            line-height: 1.6;
            font-weight: 300; 
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        .header {{
            padding: 56px 24px 36px;
            border-bottom: 1px solid var(--border-color);
            text-align: center;
        }}

        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 16px;
            background: var(--badge-bg);
            border: 1px solid var(--border-color);
            padding: 5px 14px;
            border-radius: 20px;
            font-weight: 400;
        }}

        .header h1 {{
            font-size: 34px;
            font-weight: 300;
            letter-spacing: -1.2px;
            color: var(--accent);
            margin-bottom: 16px;
            max-width: 860px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.25;
        }}

        .header p {{
            color: var(--text-muted);
            font-size: 15px;
            max-width: 680px;
            margin: 0 auto;
            line-height: 1.6;
        }}

        .action-row {{
            margin-top: 28px;
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
        }}

        .btn-primary {{
            background: #ffffff;
            color: #000000;
            font-weight: 500;
            padding: 10px 22px;
            border-radius: 5px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            transition: background 0.15s ease;
        }}

        .btn-primary:hover {{
            background: #d4d4d4;
        }}

        .btn-secondary {{
            background: transparent;
            color: #ffffff;
            border: 1px solid var(--border-color);
            font-weight: 400;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            transition: all 0.15s ease;
        }}

        .btn-secondary:hover {{
            background: #111111;
            border-color: #555555;
        }}

        .main {{
            max-width: 1120px;
            margin: 0 auto;
            padding: 40px 24px 80px;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 400;
            color: var(--accent);
            margin-top: 40px;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-color);
            letter-spacing: -0.3px;
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 28px;
            margin-bottom: 24px;
        }}

        .card h3 {{
            font-size: 15px;
            font-weight: 400;
            color: var(--accent);
            margin-bottom: 8px;
            letter-spacing: -0.2px;
        }}

        .card p.desc {{
            font-size: 13.5px;
            color: var(--text-muted);
            margin-bottom: 20px;
            line-height: 1.6;
        }}

        .controls {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 24px;
            margin-bottom: 24px;
        }}

        .slider-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
        }}

        .slider-group {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .slider-group label {{
            font-size: 13px;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
        }}

        .slider-group label span {{
            color: #ffffff;
            font-weight: 400;
        }}

        input[type="range"] {{
            -webkit-appearance: none;
            width: 100%;
            height: 4px;
            border-radius: 2px;
            background: var(--border-color);
            outline: none;
        }}

        input[type="range"]::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #ffffff;
            cursor: pointer;
            border: 2px solid var(--border-color);
        }}

        .viz-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 24px;
        }}

        @media (max-width: 900px) {{
            .viz-grid {{ grid-template-columns: 1fr; }}
            .header h1 {{ font-size: 26px; }}
        }}

        .full-width {{
            grid-column: 1 / -1;
        }}

        .chart-container {{
            position: relative;
            height: 350px;
            width: 100%;
        }}

        canvas {{
            background: transparent;
            width: 100%;
            height: 100%;
        }}

        .figure-card img {{
            width: 100%;
            height: auto;
            border-radius: 4px;
            border: 1px solid var(--border-color);
            display: block;
            background: #ffffff;
        }}

        .btn-group {{
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
        }}

        button {{
            background: var(--bg-color);
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 8px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 400;
            font-size: 13px;
            transition: all 0.2s;
        }}

        button:hover {{
            background: #111111;
            border-color: #444444;
            color: #ffffff;
        }}

        .results-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}

        .results-table th {{
            text-align: left;
            padding: 14px 12px;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border-color);
            font-weight: 400;
        }}

        .results-table td {{
            padding: 14px 12px;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-main);
        }}

        .footer {{
            margin-top: 60px;
            padding-top: 24px;
            border-top: 1px solid var(--border-color);
            text-align: center;
            color: var(--text-muted);
            font-size: 12.5px;
        }}

        .footer a {{
            color: #cccccc;
            text-decoration: none;
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="badge">Author: Dakshesh Das &bull; Independent Student Researcher</div>
        <h1>Numerical Investigation of Quantum Tunneling Through Non-Standard Barrier Geometries</h1>
        <p>A systematic computational study quantifying how potential barrier geometry alters quantum transmission by up to 10⁶&times;, introducing the WKB Shape Factor (S), and modeling wave packet scattering.</p>
        
        <div class="action-row">
            <a href="main.pdf" class="btn-primary" download>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                Download Formal Paper (PDF)
            </a>
            <a href="qm_paper.zip" class="btn-secondary" download>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
                Download LaTeX &amp; Figures (.ZIP)
            </a>
            <a href="https://github.com/dakshesh123-rgb/qm-project-website" class="btn-secondary" target="_blank">
                GitHub Repository
            </a>
        </div>
    </div>
    
    <div class="main">
        <div class="card full-width">
            <h3>Research Abstract &amp; Thesis</h3>
            <p class="desc" style="margin-bottom: 0;">
                Standard quantum mechanics textbooks almost exclusively treat tunneling through rectangular barriers due to their analytical solvability. This computational investigation demonstrates that barrier geometry introduces dramatic differences in transmission: under identical peak height (V₀ = 5.0) and width (W = 5.0), an exponential profile transmits approximately 2.3 &times; 10⁶ times more than a rectangular barrier. Using a pure Python finite-difference solver validated to sub-0.04% error against analytical benchmarks, we evaluate five geometries, define the WKB Shape Factor (S), and model diverse bound-state and scattering phenomena.
            </p>
        </div>

        <h2 class="section-title">Publication Figures (Generated via Matplotlib)</h2>
        <p style="font-size:13.5px; color:var(--text-muted); margin-bottom:20px;">Direct high-resolution figures from the formal paper exploring convergence, bound states, and scattering dynamics.</p>

        <div class="viz-grid">
            <div class="card figure-card">
                <h3>1. Barrier Profiles Overlay</h3>
                <p class="desc">The five barrier geometries (Rectangular, Parabolic, Triangular, Gaussian, Exponential) evaluated under fixed width W=3.0 and height V₀=5.0 with particle energy E=1.0.</p>
                <img src="figures/barrier_profiles.png" alt="Barrier Profiles Overlay">
            </div>

            <div class="card figure-card">
                <h3>2. Numerical Convergence Analysis</h3>
                <p class="desc">Log-log plot of relative eigenvalue error versus grid spacing &Delta;x for the infinite well ground state, confirming exact O(&Delta;x²) second-order convergence.</p>
                <img src="figures/convergence.png" alt="Numerical Convergence">
            </div>

            <div class="card figure-card">
                <h3>3. Shape Factor Correlation</h3>
                <p class="desc">Empirical correlation between the WKB-derived Shape Factor S and exact numerical transmission T at W=3.0 on a logarithmic scale.</p>
                <img src="figures/shape_factor_correlation.png" alt="Shape Factor Correlation">
            </div>

            <div class="card figure-card">
                <h3>4. Double-Well Tunnel Splitting</h3>
                <p class="desc">Symmetric ground state (&psi;₀) and antisymmetric first excited state (&psi;₁) in a double-well potential, showing the energy level splitting &Delta;E.</p>
                <img src="figures/double_well.png" alt="Double Well Tunnel Splitting">
            </div>

            <div class="card figure-card">
                <h3>5. Morse Potential Anharmonic Vibrations</h3>
                <p class="desc">Calculated molecular vibrational wavefunctions offset by their eigenvalues. Decreasing level spacing illustrates impending molecular dissociation.</p>
                <img src="figures/morse_potential.png" alt="Morse Potential">
            </div>

            <div class="card figure-card">
                <h3>6. Resonant Cavity Transmission</h3>
                <p class="desc">Transmission spectrum T(E) across a double-barrier structure showing sharp Fabry-Pérot resonant transmission peaks approaching unity.</p>
                <img src="figures/resonant_tunneling.png" alt="Resonant Tunneling">
            </div>
        </div>

        <h2 class="section-title">Interactive WKB Barrier Explorer</h2>

        <div class="controls">
            <div class="slider-grid">
                <div class="slider-group">
                    <label>Barrier Height (V₀): <span id="v0-val">10.0</span></label>
                    <input type="range" id="v0" min="1" max="30" step="0.5" value="10">
                </div>
                <div class="slider-group">
                    <label>Barrier Width (W): <span id="width-val">2.0</span></label>
                    <input type="range" id="bwidth" min="0.5" max="5" step="0.25" value="2">
                </div>
                <div class="slider-group">
                    <label>Particle Energy (E): <span id="energy-val">3.0</span></label>
                    <input type="range" id="energy" min="0.5" max="29" step="0.5" value="3">
                </div>
            </div>
        </div>

        <div class="viz-grid">
            <div class="card">
                <h3>Interactive Geometry Profiles</h3>
                <p class="desc">Dynamically updates potential curves and incident energy level as sliders adjust.</p>
                <div class="chart-container" style="height: 300px;">
                    <canvas id="barriers-canvas"></canvas>
                </div>
            </div>

            <div class="card">
                <h3>WKB Shape Factor Comparison</h3>
                <p class="desc">Calculated geometric correction coefficients relative to a rectangular barrier (S = 1.000).</p>
                <div class="chart-container" style="height: 300px;">
                    <canvas id="factor-canvas"></canvas>
                </div>
            </div>

            <div class="card full-width">
                <h3>Calculated Transmission Probabilities</h3>
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Shape</th>
                            <th>Transmission Probability (T)</th>
                            <th>Relative to Rectangular</th>
                        </tr>
                    </thead>
                    <tbody id="results-body">
                    </tbody>
                </table>
            </div>
        </div>

        <h2 class="section-title">Numerical Parameter Sweeps</h2>
        
        <div class="viz-grid">
            <div class="card">
                <h3>Logarithmic Transmission vs. Barrier Width</h3>
                <p class="desc">Numerical transmission probability (T) across width W &in; [0.5, 5.0]. Exponential slope differences reflect distinct integrated barrier areas.</p>
                <div class="chart-container">
                    <canvas id="sfChart"></canvas>
                </div>
            </div>
            
            <div class="card">
                <h3>Double Barrier Resonant Transmission</h3>
                <p class="desc">Transfer matrix sweep showing sharp transmission resonance (T &approx; 1.0) due to constructive quantum interference inside the cavity.</p>
                <div class="chart-container">
                    <canvas id="resChart"></canvas>
                </div>
            </div>
        </div>

        <h2 class="section-title">Time-Dependent Wave Packet Dynamics</h2>

        <div class="card full-width">
            <h3>Crank-Nicolson Wave Packet Collision</h3>
            <p class="desc">Time-dependent Schrödinger equation integration. A Gaussian wave packet bifurcates continuously into simultaneously propagating transmitted and reflected packets upon colliding with a potential barrier.</p>
            <div class="btn-group">
                <button id="btn-play">Play Animation</button>
                <button id="btn-reset">Reset</button>
            </div>
            <div class="chart-container">
                <canvas id="wpChart"></canvas>
            </div>
        </div>
        
        <div class="footer">
            <p>Quantum Mechanics Computational Research Project &bull; Dakshesh Das &bull; <a href="https://github.com/dakshesh123-rgb/qm-project-website" target="_blank">GitHub Repository</a> &bull; Built with pure Python, Matplotlib, and Chart.js</p>
        </div>
    </div>

<script>
    // --- 1. Interactive WKB Section ---
    const SHAPES = [
        {{ name: 'Rectangular', color: '#ffffff',  fn: (x, V0, W) => Math.abs(x) < W/2 ? V0 : 0 }},
        {{ name: 'Trapezoidal', color: '#94a3b8',  fn: (x, V0, W) => {{ 
            const d = Math.abs(x), flat = W*0.25;
            if (d < flat) return V0;
            if (d < W/2) return V0 * (1 - (d-flat)/(W/2-flat));
            return 0;
        }}}},
        {{ name: 'Parabolic',   color: '#38bdf8',  fn: (x, V0, W) => Math.abs(x) < W/2 ? V0*(1-(2*Math.abs(x)/W)**2) : 0 }},
        {{ name: 'Gaussian',    color: '#818cf8',  fn: (x, V0, W) => {{ 
            const sigma = W / (2*Math.sqrt(2*Math.log(100)));
            return V0 * Math.exp(-x*x/(2*sigma*sigma));
        }}}},
        {{ name: 'Triangular',  color: '#34d399',  fn: (x, V0, W) => Math.abs(x) < W/2 ? V0*(1-2*Math.abs(x)/W) : 0 }},
        {{ name: 'Exponential', color: '#fbbf24',  fn: (x, V0, W) => {{ 
            const alpha = 2*Math.log(100)/W;
            return V0 * Math.exp(-alpha*Math.abs(x));
        }}}},
    ];

    function wkbTunneling(shape, V0, W, E, nPoints=1000) {{
        const xMin = -W*1.5, xMax = W*1.5;
        const dx = (xMax - xMin) / nPoints;
        let integral = 0;
        for (let i = 0; i < nPoints; i++) {{
            const x = xMin + (i+0.5) * dx;
            const V = shape.fn(x, V0, W);
            if (V > E) integral += Math.sqrt(2*(V-E)) * dx;
        }}
        return Math.min(Math.exp(-2*integral), 1.0);
    }}

    function wkbExponent(shape, V0, W, E, nPoints=1000) {{
        const xMin = -W*1.5, xMax = W*1.5;
        const dx = (xMax - xMin) / nPoints;
        let integral = 0;
        for (let i = 0; i < nPoints; i++) {{
            const x = xMin + (i+0.5) * dx;
            const V = shape.fn(x, V0, W);
            if (V > E) integral += Math.sqrt(2*(V-E)) * dx;
        }}
        return 2 * integral;
    }}

    function setupCanvas(canvas) {{
        const rect = canvas.getBoundingClientRect();
        const dpr = window.devicePixelRatio || 1;
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        const ctx = canvas.getContext('2d');
        ctx.scale(dpr, dpr);
        return {{ ctx, w: rect.width, h: rect.height }};
    }}

    function drawAxes(ctx, w, h, pad, xLabel, yLabel) {{
        ctx.strokeStyle = '#222222';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(pad, pad);
        ctx.lineTo(pad, h - pad);
        ctx.lineTo(w - pad, h - pad);
        ctx.stroke();

        ctx.fillStyle = '#666666';
        ctx.font = '300 12px Inter';
        if (xLabel) ctx.fillText(xLabel, w/2, h - 10);
        if (yLabel) {{
            ctx.save();
            ctx.translate(15, h/2);
            ctx.rotate(-Math.PI/2);
            ctx.textAlign = 'center';
            ctx.fillText(yLabel, 0, 0);
            ctx.restore();
        }}
    }}

    function drawBarriers(V0, W, E) {{
        const canvas = document.getElementById('barriers-canvas');
        if(!canvas) return;
        const {{ ctx, w, h }} = setupCanvas(canvas);
        const pad = 40;
        
        ctx.clearRect(0, 0, w, h);
        drawAxes(ctx, w, h, pad, 'Position (x)', 'V(x)');

        const xMin = -W*2, xMax = W*2;
        const yMax = V0 * 1.3;

        function toScreen(x, y) {{
            return [
                pad + (x - xMin)/(xMax - xMin) * (w - 2*pad),
                (h - pad) - y/yMax * (h - 2*pad)
            ];
        }}

        // Energy line
        const [eX1, eY] = toScreen(xMin, E);
        const [eX2, _] = toScreen(xMax, E);
        ctx.strokeStyle = '#666666';
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(eX1, eY);
        ctx.lineTo(eX2, eY);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#aaaaaa';
        ctx.font = '300 11px Inter';
        ctx.fillText(`E = ${{E.toFixed(1)}}`, eX2 - 45, eY - 8);

        const nPoints = 300;
        SHAPES.forEach((shape) => {{
            ctx.strokeStyle = shape.color;
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            for (let i = 0; i <= nPoints; i++) {{
                const x = xMin + (xMax-xMin) * i/nPoints;
                const V = shape.fn(x, V0, W);
                const [sx, sy] = toScreen(x, V);
                if (i === 0) ctx.moveTo(sx, sy);
                else ctx.lineTo(sx, sy);
            }}
            ctx.stroke();
        }});

        ctx.fillStyle = '#555555';
        ctx.font = '300 10px Inter';
        for (let v = 0; v <= yMax; v += Math.ceil(yMax/5)) {{
            const [_, sy] = toScreen(0, v);
            ctx.fillText(v.toFixed(0), 10, sy + 4);
        }}
    }}

    function drawShapeFactor(V0, W, E) {{
        const canvas = document.getElementById('factor-canvas');
        if(!canvas) return;
        const {{ ctx, w, h }} = setupCanvas(canvas);
        const pad = 40;

        ctx.clearRect(0, 0, w, h);

        const gammaRect = wkbExponent(SHAPES[0], V0, W, E);
        const barH = (h - 2*pad) / SHAPES.length - 8;

        SHAPES.forEach((shape, i) => {{
            const gamma = wkbExponent(shape, V0, W, E);
            const S = gammaRect > 0 ? gamma / gammaRect : 0;
            const y = pad + i * (barH + 8);
            const barW = S * (w - pad - 120);

            ctx.fillStyle = shape.color;
            ctx.globalAlpha = 0.2;
            ctx.fillRect(100, y, barW, barH);
            
            ctx.globalAlpha = 1.0;
            ctx.strokeStyle = shape.color;
            ctx.lineWidth = 1;
            ctx.strokeRect(100, y, barW, barH);

            ctx.fillStyle = '#cccccc';
            ctx.font = '300 12px Inter';
            ctx.textAlign = 'right';
            ctx.fillText(shape.name, 90, y + barH/2 + 4);

            ctx.fillStyle = '#888888';
            ctx.textAlign = 'left';
            ctx.fillText(`S = ${{S.toFixed(3)}}`, barW + 110, y + barH/2 + 4);
        }});
        ctx.textAlign = 'left';
    }}

    function updateTable(V0, W, E) {{
        const tbody = document.getElementById('results-body');
        if(!tbody) return;
        
        if (E >= V0) {{
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#666666;padding:20px;">Energy ≥ Barrier Height: Classical transmission (No tunneling)</td></tr>';
            return;
        }}

        let results = SHAPES.map(shape => ({{
            shape,
            T: wkbTunneling(shape, V0, W, E)
        }}));
        
        results.sort((a, b) => b.T - a.T);
        
        const rectT = results.find(r => r.shape.name === 'Rectangular').T;

        tbody.innerHTML = results.map((r, i) => {{
            const ratio = rectT > 0 ? (r.T / rectT) : 0;
            let ratioText = ratio >= 1e6 ? (ratio/1e6).toFixed(1) + 'M ×' : 
                            ratio >= 1000 ? (ratio/1000).toFixed(1) + 'k ×' : 
                            ratio.toFixed(1) + ' ×';
            if (r.shape.name === 'Rectangular') ratioText = '1.0 × (Baseline)';

            return `
                <tr>
                    <td style="color: #888;">${{i + 1}}</td>
                    <td><span style="color: ${{r.shape.color}}; font-size: 16px;">■</span> <span style="font-weight: 400; margin-left: 4px;">${{r.shape.name}}</span></td>
                    <td style="font-family: monospace;">${{r.T.toExponential(4)}}</td>
                    <td style="color: #ccc;">${{ratioText}}</td>
                </tr>
            `;
        }}).join('');
    }}

    function updateAll() {{
        const V0 = parseFloat(document.getElementById('v0').value);
        const W = parseFloat(document.getElementById('bwidth').value);
        const E = parseFloat(document.getElementById('energy').value);

        document.getElementById('v0-val').textContent = V0.toFixed(1);
        document.getElementById('width-val').textContent = W.toFixed(2);
        document.getElementById('energy-val').textContent = E.toFixed(1);

        drawBarriers(V0, W, E);
        drawShapeFactor(V0, W, E);
        updateTable(V0, W, E);
    }}

    document.getElementById('v0').addEventListener('input', updateAll);
    document.getElementById('bwidth').addEventListener('input', updateAll);
    document.getElementById('energy').addEventListener('input', updateAll);
    window.addEventListener('load', updateAll);


    // --- 2. Chart.js Numerical Solver Data ---
    const sfData = {json.dumps(sf_data)};
    const resData = {json.dumps(res_data)};
    const wpData = {json.dumps(wp_data)};

    Chart.defaults.color = '#888888';
    Chart.defaults.font.family = 'Inter';
    Chart.defaults.font.weight = 300;
    Chart.defaults.scale.grid.color = '#151515';
    Chart.defaults.scale.grid.borderColor = '#222222';

    const getT = (logArray) => logArray.map(val => Math.pow(10, val));
    const sfFormattedWidths = sfData.widths.map(w => w.toFixed(1));

    const ctxSf = document.getElementById('sfChart').getContext('2d');
    new Chart(ctxSf, {{
        type: 'line',
        data: {{
            labels: sfFormattedWidths,
            datasets: [
                {{ label: 'Rectangular', data: getT(sfData.Rectangular), borderColor: '#ffffff', borderWidth: 1.5, fill: false, tension: 0.1, pointRadius: 0 }},
                {{ label: 'Gaussian', data: getT(sfData.Gaussian), borderColor: '#818cf8', borderWidth: 1.5, fill: false, tension: 0.4, pointRadius: 0 }},
                {{ label: 'Triangular', data: getT(sfData.Triangular), borderColor: '#34d399', borderWidth: 1.5, fill: false, tension: 0.4, pointRadius: 0 }},
                {{ label: 'Exponential', data: getT(sfData.Exponential), borderColor: '#fbbf24', borderWidth: 1.5, fill: false, tension: 0.4, pointRadius: 0 }}
            ]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            scales: {{
                x: {{ title: {{ display: true, text: 'Barrier Width (W)' }} }},
                y: {{ 
                    type: 'logarithmic',
                    min: 1e-12,
                    max: 1,
                    title: {{ display: true, text: 'Transmission (T)' }} 
                }}
            }},
            plugins: {{ legend: {{ labels: {{ usePointStyle: true, boxWidth: 6, color: '#e0e0e0' }} }} }}
        }}
    }});

    const ctxRes = document.getElementById('resChart').getContext('2d');
    const resFormattedEnergies = resData.energies.map(e => e.toFixed(2));
    new Chart(ctxRes, {{
        type: 'line',
        data: {{
            labels: resFormattedEnergies,
            datasets: [
                {{
                    label: 'Transmission',
                    data: resData.transmissions,
                    borderColor: '#38bdf8',
                    borderWidth: 1.5,
                    fill: false,
                    tension: 0.1,
                    pointRadius: 0
                }}
            ]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            scales: {{
                x: {{ title: {{ display: true, text: 'Particle Energy (E)' }}, ticks: {{ maxTicksLimit: 8 }} }},
                y: {{ min: 0, max: 1.05, title: {{ display: true, text: 'Transmission (T)' }} }}
            }},
            plugins: {{ legend: {{ display: false }} }}
        }}
    }});

    const ctxWp = document.getElementById('wpChart').getContext('2d');
    const xFormatted = wpData.x.map(val => val.toFixed(1));
    const vScaled = wpData.V.map(v => v * 0.15); 

    let currentFrame = 0;
    let animationId = null;

    const wpChart = new Chart(ctxWp, {{
        type: 'line',
        data: {{
            labels: xFormatted,
            datasets: [
                {{
                    label: 'Barrier Potential',
                    data: vScaled,
                    borderColor: '#333333',
                    backgroundColor: 'rgba(51, 51, 51, 0.4)',
                    borderWidth: 1,
                    fill: true,
                    tension: 0,
                    pointRadius: 0
                }},
                {{
                    label: 'Probability Density',
                    data: wpData.frames[0],
                    borderColor: '#ffffff',
                    borderWidth: 1.5,
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0
                }}
            ]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            scales: {{
                x: {{ title: {{ display: true, text: 'Position (x)' }}, ticks: {{ maxTicksLimit: 10 }} }},
                y: {{ min: 0, max: 0.3, title: {{ display: true, text: 'Amplitude' }} }}
            }},
            plugins: {{ legend: {{ labels: {{ usePointStyle: true, boxWidth: 6, color: '#e0e0e0' }} }} }}
        }}
    }});

    function playFrame() {{
        currentFrame++;
        if (currentFrame >= wpData.frames.length) {{
            cancelAnimationFrame(animationId);
            return;
        }}
        wpChart.data.datasets[1].data = wpData.frames[currentFrame];
        wpChart.update();
        setTimeout(() => {{
            animationId = requestAnimationFrame(playFrame);
        }}, 35);
    }}

    document.getElementById('btn-play').addEventListener('click', () => {{
        if (currentFrame >= wpData.frames.length - 1) currentFrame = 0;
        if (animationId) cancelAnimationFrame(animationId);
        animationId = requestAnimationFrame(playFrame);
    }});

    document.getElementById('btn-reset').addEventListener('click', () => {{
        if (animationId) cancelAnimationFrame(animationId);
        currentFrame = 0;
        wpChart.data.datasets[1].data = wpData.frames[0];
        wpChart.update();
    }});

</script>
</body>
</html>
"""

with open("/root/qm_project/web/index.html", "w") as f:
    f.write(html_content)

print("index.html successfully updated with Publication Figures and Paper Download links.")
