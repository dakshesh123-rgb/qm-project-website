import json

# Read data files
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
    <title>Quantum Tunneling Explorer</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #000000;
            --card-bg: #0d0d0d;
            --border-color: #222222;
            --text-main: #f0f0f0;
            --text-muted: #888888;
            --accent-blue: #3b82f6;
            --accent-red: #ef4444;
            --accent-yellow: #f59e0b;
            --accent-green: #10b981;
            --accent-purple: #8b5cf6;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Inter', system-ui, sans-serif;
            background: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            line-height: 1.6;
            font-weight: 300;
        }}

        .header {{
            padding: 40px 32px 20px;
            border-bottom: 1px solid var(--border-color);
            text-align: center;
            background: var(--bg-color);
        }}

        .header h1 {{
            font-size: 32px;
            font-weight: 600;
            letter-spacing: -0.5px;
            color: #ffffff;
            margin-bottom: 12px;
        }}

        .header p {{
            color: var(--text-muted);
            font-size: 16px;
            max-width: 600px;
            margin: 0 auto;
        }}

        .main {{
            max-width: 1280px;
            margin: 0 auto;
            padding: 32px 24px;
        }}

        .section-title {{
            font-size: 20px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-color);
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 24px;
        }}

        .card h3 {{
            font-size: 15px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 16px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .card p {{
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 16px;
        }}

        .controls {{
            background: var(--bg-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 32px;
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
            font-weight: 600;
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
            margin-bottom: 32px;
        }}

        @media (max-width: 900px) {{
            .viz-grid {{ grid-template-columns: 1fr; }}
        }}

        .full-width {{
            grid-column: 1 / -1;
        }}

        canvas {{
            width: 100%;
            height: 300px;
            border-radius: 4px;
            background: var(--bg-color);
            border: 1px solid var(--border-color);
        }}

        .results-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}

        .results-table th {{
            text-align: left;
            padding: 12px;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border-color);
            font-weight: 600;
        }}

        .results-table td {{
            padding: 12px;
            border-bottom: 1px solid #1a1a1a;
            color: var(--text-main);
        }}

        .btn-group {{
            display: flex;
            gap: 12px;
            margin-top: 20px;
            justify-content: center;
        }}

        button {{
            background: var(--bg-color);
            color: #ffffff;
            border: 1px solid var(--border-color);
            padding: 10px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 13px;
            transition: all 0.2s;
        }}

        button:hover {{
            background: #1a1a1a;
            border-color: #333333;
        }}

        .primary-btn {{
            background: #ffffff;
            color: #000000;
            border: none;
        }}

        .primary-btn:hover {{
            background: #e0e0e0;
        }}

    </style>
</head>
<body>
    <div class="header">
        <h1>Quantum Tunneling Explorer</h1>
        <p>A computational study on barrier geometry, resonant tunneling, and wave packet dynamics.</p>
    </div>
    
    <div class="main">
        <div class="card full-width">
            <h3>Overview</h3>
            <p>
                Standard quantum mechanics texts primarily analyze tunneling through rectangular barriers. Our computational research reveals that the geometric shape of a barrier drastically alters the quantum tunneling probability. Because transmission scales exponentially with the barrier's area, geometric shapes with lower average profiles (e.g., exponential, Gaussian) exhibit orders of magnitude higher transmission than a standard rectangular barrier of the exact same maximum height and width. 
            </p>
            <p>
                This dashboard presents interactive WKB approximation models alongside exact finite-difference numerical solver data to quantify this phenomenon.
            </p>
        </div>

        <h2 class="section-title">Interactive WKB Analysis</h2>

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
                <h3>Barrier Geometry Profiles</h3>
                <p>Comparison of six barrier shapes with identical maximum height and width.</p>
                <canvas id="barriers-canvas" height="300"></canvas>
            </div>

            <div class="card">
                <h3>Shape Factor Analysis</h3>
                <p>Calculated geometric correction coefficients relative to a rectangular barrier.</p>
                <canvas id="factor-canvas" height="300"></canvas>
            </div>

            <div class="card full-width">
                <h3>Tunneling Probability by Shape</h3>
                <table class="results-table" id="results-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Barrier Shape</th>
                            <th>Tunneling Probability (T)</th>
                            <th>Transmission Ratio (vs Rectangular)</th>
                        </tr>
                    </thead>
                    <tbody id="results-body"></tbody>
                </table>
            </div>
        </div>

        <h2 class="section-title">Exact Numerical Solver Data</h2>
        
        <div class="viz-grid">
            <div class="card">
                <h3>Quantum Leakage vs Barrier Geometry</h3>
                <p>Finite-difference Transfer Matrix calculations of transmission vs width.</p>
                <canvas id="sfChart" height="300"></canvas>
            </div>
            
            <div class="card">
                <h3>Resonant Tunneling</h3>
                <p>Multi-barrier transmission proving constructive interference.</p>
                <canvas id="resChart" height="300"></canvas>
            </div>
        </div>

        <h2 class="section-title">Time-Dependent Dynamics</h2>

        <div class="card full-width">
            <h3>Wave Packet Collision</h3>
            <p>
                Crank-Nicolson integration of the Time-Dependent Schrödinger Equation (TDSE).
                The visualization shows a Gaussian wave packet colliding with a potential barrier, illustrating quantum superposition through simultaneous reflection and tunneling.
            </p>
            
            <div style="display: flex; flex-direction: column; align-items: center; margin-top: 24px;">
                <canvas id="wpChart" height="350" style="width:100%; max-width:900px; border:none; background:#050505;"></canvas>
                <div class="btn-group">
                    <button id="btn-play" class="primary-btn">Play Simulation</button>
                    <button id="btn-reset">Reset</button>
                </div>
            </div>
        </div>

    </div>

<script>
    // Exact Numerical Data
    const sfData = {json.dumps(sf_data)};
    const resData = {json.dumps(res_data)};
    const wpData = {json.dumps(wp_data)};

    // Setup global chart defaults for professional dark theme
    Chart.defaults.color = '#888888';
    Chart.defaults.font.family = 'Inter';
    Chart.defaults.scale.grid.color = '#1a1a1a';
    
    // Custom Chart initialization
    document.addEventListener("DOMContentLoaded", function() {{
        // Quantum Leakage Chart
        const ctxSf = document.getElementById('sfChart').getContext('2d');
        const sfFormattedWidths = sfData.widths.map(w => w.toFixed(1));
        new Chart(ctxSf, {{
            type: 'line',
            data: {{
                labels: sfFormattedWidths,
                datasets: [
                    {{ label: 'Rectangular', data: sfData.Rectangular, borderColor: '#ef4444', borderWidth: 2, fill: false, tension: 0.1 }},
                    {{ label: 'Gaussian', data: sfData.Gaussian, borderColor: '#3b82f6', borderWidth: 2, fill: false, tension: 0.4 }},
                    {{ label: 'Triangular', data: sfData.Triangular, borderColor: '#10b981', borderWidth: 2, fill: false, tension: 0.4 }},
                    {{ label: 'Exponential', data: sfData.Exponential, borderColor: '#8b5cf6', borderWidth: 2, fill: false, tension: 0.4 }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ title: {{ display: true, text: 'Barrier Width (W)', color: '#888' }} }},
                    y: {{ title: {{ display: true, text: 'Log10(Transmission)', color: '#888' }} }}
                }},
                plugins: {{ legend: {{ labels: {{ color: '#ccc' }} }} }}
            }}
        }});

        // Resonant Tunneling Chart
        const ctxRes = document.getElementById('resChart').getContext('2d');
        const resFormattedEnergies = resData.energies.map(e => e.toFixed(2));
        new Chart(ctxRes, {{
            type: 'line',
            data: {{
                labels: resFormattedEnergies,
                datasets: [
                    {{
                        label: 'Transmission T(E)',
                        data: resData.transmissions,
                        borderColor: '#f59e0b',
                        backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.1,
                        pointRadius: 0
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ title: {{ display: true, text: 'Particle Energy (E)', color: '#888' }}, ticks: {{ maxTicksLimit: 10 }} }},
                    y: {{ title: {{ display: true, text: 'Transmission T', color: '#888' }} }}
                }},
                plugins: {{ legend: {{ labels: {{ color: '#ccc' }} }} }}
            }}
        }});

        // Wave Packet Chart
        const ctxWp = document.getElementById('wpChart').getContext('2d');
        const xFormatted = wpData.x.map(val => val.toFixed(1));
        const vScaled = wpData.V.map(v => v * 0.2); 

        let currentFrame = 0;
        let animationId = null;

        const wpChart = new Chart(ctxWp, {{
            type: 'line',
            data: {{
                labels: xFormatted,
                datasets: [
                    {{
                        label: 'Potential Barrier V(x)',
                        data: vScaled,
                        borderColor: '#444444',
                        backgroundColor: 'rgba(68, 68, 68, 0.2)',
                        borderWidth: 1,
                        fill: true,
                        tension: 0,
                        pointRadius: 0
                    }},
                    {{
                        label: 'Probability Density |Ψ(x,t)|²',
                        data: wpData.frames[0],
                        borderColor: '#ffffff',
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 2,
                        fill: true,
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
                    x: {{ title: {{ display: true, text: 'Position x', color: '#888' }}, ticks: {{ maxTicksLimit: 10 }} }},
                    y: {{ title: {{ display: true, text: '|Ψ|²', color: '#888' }}, min: 0, max: 0.4 }}
                }},
                plugins: {{ legend: {{ labels: {{ color: '#ccc' }} }} }}
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
            }}, 40);
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
    }});

    // WKB Functions & Canvas Drawing
    const SHAPES = [
        {{ name: 'Rectangular', color: '#ef4444',  fn: (x, V0, W) => Math.abs(x) < W/2 ? V0 : 0 }},
        {{ name: 'Trapezoidal', color: '#f59e0b',  fn: (x, V0, W) => {{
            const d = Math.abs(x), flat = W*0.25;
            if (d < flat) return V0;
            if (d < W/2) return V0 * (1 - (d-flat)/(W/2-flat));
            return 0;
        }}}},
        {{ name: 'Parabolic',   color: '#eab308',  fn: (x, V0, W) => Math.abs(x) < W/2 ? V0*(1-(2*Math.abs(x)/W)**2) : 0 }},
        {{ name: 'Gaussian',    color: '#3b82f6',  fn: (x, V0, W) => {{
            const sigma = W / (2*Math.sqrt(2*Math.log(100)));
            return V0 * Math.exp(-x*x/(2*sigma*sigma));
        }}}},
        {{ name: 'Triangular',  color: '#10b981',  fn: (x, V0, W) => Math.abs(x) < W/2 ? V0*(1-2*Math.abs(x)/W) : 0 }},
        {{ name: 'Exponential', color: '#8b5cf6',  fn: (x, V0, W) => {{
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
        ctx.strokeStyle = '#333333';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(pad, pad);
        ctx.lineTo(pad, h - pad);
        ctx.lineTo(w - pad, h - pad);
        ctx.stroke();

        ctx.fillStyle = '#888888';
        ctx.font = '12px Inter';
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
        ctx.strokeStyle = '#ffffff';
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(eX1, eY);
        ctx.lineTo(eX2, eY);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#ffffff';
        ctx.font = '12px Inter';
        ctx.fillText(`E = ${{E}}`, eX2 - 50, eY - 8);

        const nPoints = 300;
        SHAPES.forEach((shape, si) => {{
            ctx.strokeStyle = shape.color;
            ctx.lineWidth = 2;
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

        // Y-axis labels
        ctx.fillStyle = '#666666';
        ctx.font = '11px Inter';
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

            ctx.fillStyle = shape.color + '44';
            ctx.fillRect(100, y, barW, barH);
            ctx.strokeStyle = shape.color;
            ctx.lineWidth = 1;
            ctx.strokeRect(100, y, barW, barH);

            ctx.fillStyle = '#ffffff';
            ctx.font = '12px Inter';
            ctx.textAlign = 'right';
            ctx.fillText(shape.name, 90, y + barH/2 + 4);

            ctx.fillStyle = '#cccccc';
            ctx.textAlign = 'left';
            ctx.fillText(`S = ${{S.toFixed(3)}}`, barW + 110, y + barH/2 + 4);
        }});
        ctx.textAlign = 'left';
    }}

    function updateTable(V0, W, E) {{
        const tbody = document.getElementById('results-body');
        if(!tbody) return;
        
        if (E >= V0) {{
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#ef4444;padding:20px;">Energy ≥ Barrier Height: Classical transmission (No tunneling)</td></tr>';
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
                    <td style="color: #fff; font-weight: 600;">${{i + 1}}</td>
                    <td><span style="color: ${{r.shape.color}}">■</span> ${{r.shape.name}}</td>
                    <td style="font-family: monospace;">${{r.T.toExponential(4)}}</td>
                    <td style="color: #fff;">${{ratioText}}</td>
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

    // Initial draw
    window.addEventListener('load', updateAll);
</script>
</body>
</html>
"""

with open("/root/qm_project/web/index.html", "w") as f:
    f.write(html_content)

print("HTML rewritten cleanly.")
