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
    <title>Quantum Tunneling Explorer</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #000000;
            --card-bg: #080808;
            --border-color: #222222;
            --text-main: #e0e0e0;
            --text-muted: #888888;
            --accent-primary: #ffffff;
            --accent-blue: #3b82f6;
            --accent-green: #10b981;
            --accent-orange: #f59e0b;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Inter', system-ui, sans-serif;
            background: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            line-height: 1.5;
            font-weight: 300;
            -webkit-font-smoothing: antialiased;
        }}

        .header {{
            padding: 48px 32px 32px;
            border-bottom: 1px solid var(--border-color);
            text-align: center;
            background: var(--bg-color);
        }}

        .header h1 {{
            font-size: 28px;
            font-weight: 500;
            letter-spacing: -0.5px;
            color: var(--accent-primary);
            margin-bottom: 12px;
        }}

        .header p {{
            color: var(--text-muted);
            font-size: 15px;
            max-width: 600px;
            margin: 0 auto;
        }}

        .main {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 24px;
        }}

        .section-title {{
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-color);
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 24px;
            margin-bottom: 24px;
        }}

        .card h3 {{
            font-size: 14px;
            font-weight: 500;
            color: var(--accent-primary);
            margin-bottom: 8px;
        }}

        .card p {{
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 20px;
        }}

        .controls {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 24px;
            margin-bottom: 32px;
        }}

        .slider-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 32px;
        }}

        .slider-group {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .slider-group label {{
            font-size: 12px;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .slider-group label span {{
            color: var(--accent-primary);
            font-weight: 500;
        }}

        input[type="range"] {{
            -webkit-appearance: none;
            width: 100%;
            height: 2px;
            background: var(--border-color);
            outline: none;
        }}

        input[type="range"]::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--accent-primary);
            cursor: pointer;
        }}

        .viz-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 48px;
        }}

        @media (max-width: 900px) {{
            .viz-grid {{ grid-template-columns: 1fr; }}
        }}

        .full-width {{
            grid-column: 1 / -1;
        }}

        canvas {{
            width: 100%;
            height: 250px;
            background: transparent;
        }}

        .results-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}

        .results-table th {{
            text-align: left;
            padding: 12px 16px;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border-color);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 11px;
        }}

        .results-table td {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-main);
        }}
        
        .results-table tr:last-child td {{
            border-bottom: none;
        }}

        .btn-group {{
            display: flex;
            gap: 12px;
            margin-top: 24px;
            justify-content: center;
        }}

        button {{
            background: transparent;
            color: var(--text-muted);
            border: 1px solid var(--border-color);
            padding: 8px 24px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 500;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: all 0.2s;
        }}

        button:hover {{
            color: var(--accent-primary);
            border-color: #444;
        }}

        .primary-btn {{
            background: var(--accent-primary);
            color: var(--bg-color);
            border: none;
        }}

        .primary-btn:hover {{
            background: #cccccc;
            color: var(--bg-color);
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
                Standard quantum mechanics texts primarily analyze tunneling through rectangular barriers. Our computational research reveals that the geometric shape of a barrier drastically alters the quantum tunneling probability. Geometric shapes with lower average profiles exhibit orders of magnitude higher transmission than a rectangular barrier of the exact same maximum height and width.
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
                <p>Comparison of barrier shapes with identical maximum height and width.</p>
                <canvas id="barriers-canvas" height="250"></canvas>
            </div>

            <div class="card">
                <h3>Shape Factor Analysis</h3>
                <p>Calculated geometric correction coefficients relative to a rectangular barrier.</p>
                <canvas id="factor-canvas" height="250"></canvas>
            </div>

            <div class="card full-width">
                <h3>Tunneling Probability by Shape</h3>
                <table class="results-table" id="results-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Barrier Shape</th>
                            <th>Tunneling Probability (T)</th>
                            <th>Transmission Ratio</th>
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
                <p>Transfer Matrix calculations of transmission probability vs barrier width.</p>
                <canvas id="sfChart" height="250"></canvas>
            </div>
            
            <div class="card">
                <h3>Resonant Tunneling</h3>
                <p>Multi-barrier transmission proving constructive interference at specific energies.</p>
                <canvas id="resChart" height="250"></canvas>
            </div>
        </div>

        <h2 class="section-title">Time-Dependent Dynamics</h2>

        <div class="card full-width">
            <h3>Wave Packet Collision</h3>
            <p>
                Time-Dependent Schrödinger Equation (TDSE) simulation of a wave packet colliding with a potential barrier.
            </p>
            
            <div style="display: flex; flex-direction: column; align-items: center; margin-top: 16px;">
                <div style="width: 100%; max-width: 800px; height: 250px; position: relative;">
                    <canvas id="wpChart"></canvas>
                </div>
                <div class="btn-group">
                    <button id="btn-play" class="primary-btn">Play Simulation</button>
                    <button id="btn-reset">Reset</button>
                </div>
            </div>
        </div>

    </div>

<script>
    const sfData = {json.dumps(sf_data)};
    const resData = {json.dumps(res_data)};
    const wpData = {json.dumps(wp_data)};

    Chart.defaults.color = '#666666';
    Chart.defaults.font.family = 'Inter';
    Chart.defaults.font.size = 11;
    Chart.defaults.scale.grid.color = '#111111';
    
    document.addEventListener("DOMContentLoaded", function() {{
        // sfChart
        const ctxSf = document.getElementById('sfChart').getContext('2d');
        const sfFormattedWidths = sfData.widths.map(w => w.toFixed(1));
        
        // Convert Log10(T) to T to avoid going to negative infinity
        const getT = (logArray) => logArray.map(val => Math.pow(10, val));

        new Chart(ctxSf, {{
            type: 'line',
            data: {{
                labels: sfFormattedWidths,
                datasets: [
                    {{ label: 'Rectangular', data: getT(sfData.Rectangular), borderColor: '#555555', borderWidth: 1.5, fill: false, tension: 0.1, pointRadius: 0 }},
                    {{ label: 'Gaussian', data: getT(sfData.Gaussian), borderColor: '#3b82f6', borderWidth: 1.5, fill: false, tension: 0.4, pointRadius: 0 }},
                    {{ label: 'Triangular', data: getT(sfData.Triangular), borderColor: '#10b981', borderWidth: 1.5, fill: false, tension: 0.4, pointRadius: 0 }},
                    {{ label: 'Exponential', data: getT(sfData.Exponential), borderColor: '#f59e0b', borderWidth: 1.5, fill: false, tension: 0.4, pointRadius: 0 }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ title: {{ display: true, text: 'Barrier Width (W)', color: '#666' }}, grid: {{ color: '#1a1a1a' }} }},
                    y: {{ 
                        type: 'logarithmic',
                        min: 1e-12,
                        title: {{ display: true, text: 'Transmission (T)', color: '#666' }},
                        grid: {{ color: '#1a1a1a' }}
                    }}
                }},
                plugins: {{ legend: {{ labels: {{ color: '#aaa', usePointStyle: true, boxWidth: 6 }} }} }}
            }}
        }});

        // resChart
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
                        borderColor: '#ffffff',
                        backgroundColor: 'rgba(255, 255, 255, 0.05)',
                        borderWidth: 1.5,
                        fill: true,
                        tension: 0.2,
                        pointRadius: 0
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ title: {{ display: true, text: 'Particle Energy (E)', color: '#666' }}, ticks: {{ maxTicksLimit: 8 }}, grid: {{ color: '#1a1a1a' }} }},
                    y: {{ title: {{ display: true, text: 'Transmission T', color: '#666' }}, min: 0, max: 1.05, grid: {{ color: '#1a1a1a' }} }}
                }},
                plugins: {{ legend: {{ display: false }} }}
            }}
        }});

        // wpChart
        const ctxWp = document.getElementById('wpChart').getContext('2d');
        // Reduce the length of the data to display for visual neatness and logic preservation
        // Use a subset of x and frames to zoom in and make it shorter
        const trimEdge = 40; 
        const xTrimmed = wpData.x.slice(trimEdge, wpData.x.length - trimEdge).map(val => val.toFixed(1));
        const vScaled = wpData.V.slice(trimEdge, wpData.x.length - trimEdge).map(v => v * 0.15); 
        
        let currentFrame = 0;
        let animationId = null;

        const wpChart = new Chart(ctxWp, {{
            type: 'line',
            data: {{
                labels: xTrimmed,
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
                        label: 'Probability Density |Ψ|²',
                        data: wpData.frames[0].slice(trimEdge, wpData.x.length - trimEdge),
                        borderColor: '#ffffff',
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1.5,
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
                    x: {{ title: {{ display: true, text: 'Position x', color: '#666' }}, ticks: {{ maxTicksLimit: 10 }}, grid: {{ display: false }} }},
                    y: {{ title: {{ display: true, text: '|Ψ|²', color: '#666' }}, min: 0, max: 0.3, grid: {{ color: '#1a1a1a' }} }}
                }},
                plugins: {{ legend: {{ labels: {{ color: '#aaa', usePointStyle: true, boxWidth: 6 }} }} }}
            }}
        }});

        function playFrame() {{
            // Increase speed by skipping frames to make it shorter and punchier
            currentFrame += 1;
            if (currentFrame >= wpData.frames.length) {{
                cancelAnimationFrame(animationId);
                return;
            }}
            wpChart.data.datasets[1].data = wpData.frames[currentFrame].slice(trimEdge, wpData.x.length - trimEdge);
            wpChart.update();
            setTimeout(() => {{
                animationId = requestAnimationFrame(playFrame);
            }}, 30);
        }}

        document.getElementById('btn-play').addEventListener('click', () => {{
            if (currentFrame >= wpData.frames.length - 1) currentFrame = 0;
            if (animationId) cancelAnimationFrame(animationId);
            animationId = requestAnimationFrame(playFrame);
        }});

        document.getElementById('btn-reset').addEventListener('click', () => {{
            if (animationId) cancelAnimationFrame(animationId);
            currentFrame = 0;
            wpChart.data.datasets[1].data = wpData.frames[0].slice(trimEdge, wpData.x.length - trimEdge);
            wpChart.update();
        }});
    }});

    const SHAPES = [
        {{ name: 'Rectangular', color: '#555555',  fn: (x, V0, W) => Math.abs(x) < W/2 ? V0 : 0 }},
        {{ name: 'Trapezoidal', color: '#888888',  fn: (x, V0, W) => {{
            const d = Math.abs(x), flat = W*0.25;
            if (d < flat) return V0;
            if (d < W/2) return V0 * (1 - (d-flat)/(W/2-flat));
            return 0;
        }}}},
        {{ name: 'Parabolic',   color: '#a3a3a3',  fn: (x, V0, W) => Math.abs(x) < W/2 ? V0*(1-(2*Math.abs(x)/W)**2) : 0 }},
        {{ name: 'Gaussian',    color: '#3b82f6',  fn: (x, V0, W) => {{
            const sigma = W / (2*Math.sqrt(2*Math.log(100)));
            return V0 * Math.exp(-x*x/(2*sigma*sigma));
        }}}},
        {{ name: 'Triangular',  color: '#10b981',  fn: (x, V0, W) => Math.abs(x) < W/2 ? V0*(1-2*Math.abs(x)/W) : 0 }},
        {{ name: 'Exponential', color: '#f59e0b',  fn: (x, V0, W) => {{
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

    function drawBarriers(V0, W, E) {{
        const canvas = document.getElementById('barriers-canvas');
        if(!canvas) return;
        const {{ ctx, w, h }} = setupCanvas(canvas);
        const pad = 30;
        
        ctx.clearRect(0, 0, w, h);
        
        const xMin = -W*2, xMax = W*2;
        const yMax = V0 * 1.3;

        function toScreen(x, y) {{
            return [
                pad + (x - xMin)/(xMax - xMin) * (w - 2*pad),
                (h - pad) - y/yMax * (h - 2*pad)
            ];
        }}

        // Axes
        ctx.strokeStyle = '#222222';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(pad, pad);
        ctx.lineTo(pad, h - pad);
        ctx.lineTo(w - pad, h - pad);
        ctx.stroke();

        // Energy line
        const [eX1, eY] = toScreen(xMin, E);
        const [eX2, _] = toScreen(xMax, E);
        ctx.strokeStyle = '#666666';
        ctx.setLineDash([3, 3]);
        ctx.beginPath();
        ctx.moveTo(eX1, eY);
        ctx.lineTo(eX2, eY);
        ctx.stroke();
        ctx.setLineDash([]);
        
        ctx.fillStyle = '#888888';
        ctx.font = '10px Inter';
        ctx.fillText(`E=${{E.toFixed(1)}}`, eX2 - 40, eY - 6);

        const nPoints = 200;
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
    }}

    function drawShapeFactor(V0, W, E) {{
        const canvas = document.getElementById('factor-canvas');
        if(!canvas) return;
        const {{ ctx, w, h }} = setupCanvas(canvas);
        const pad = 30;

        ctx.clearRect(0, 0, w, h);

        const gammaRect = wkbExponent(SHAPES[0], V0, W, E);
        const barH = (h - 2*pad) / SHAPES.length - 6;

        SHAPES.forEach((shape, i) => {{
            const gamma = wkbExponent(shape, V0, W, E);
            const S = gammaRect > 0 ? gamma / gammaRect : 0;
            const y = pad + i * (barH + 6);
            const barW = S * (w - pad - 120);

            ctx.fillStyle = shape.color + '22';
            ctx.fillRect(80, y, barW, barH);
            ctx.strokeStyle = shape.color;
            ctx.lineWidth = 1;
            ctx.strokeRect(80, y, barW, barH);

            ctx.fillStyle = '#aaaaaa';
            ctx.font = '11px Inter';
            ctx.textAlign = 'right';
            ctx.fillText(shape.name, 70, y + barH/2 + 4);

            ctx.fillStyle = '#888888';
            ctx.textAlign = 'left';
            ctx.fillText(S.toFixed(3), 80 + barW + 10, y + barH/2 + 4);
        }});
    }}

    function updateTable(V0, W, E) {{
        const tbody = document.getElementById('results-body');
        if(!tbody) return;
        
        if (E >= V0) {{
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#888;padding:20px;">Classical transmission (No tunneling)</td></tr>';
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
            if (r.shape.name === 'Rectangular') ratioText = '1.0 ×';

            return `
                <tr>
                    <td style="color: #666;">0${{i + 1}}</td>
                    <td style="color: ${{r.shape.color}}">${{r.shape.name}}</td>
                    <td style="font-family: monospace; color: #aaa;">${{r.T.toExponential(2)}}</td>
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
</script>
</body>
</html>
"""

with open("/root/qm_project/web/index.html", "w") as f:
    f.write(html_content)

print("Professional HTML written.")
