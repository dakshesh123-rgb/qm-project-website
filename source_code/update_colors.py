import re
import os

with open('/root/qm_project/web/index.html', 'r') as f:
    content = f.read()

# Replace colorful gradient header text
content = content.replace('background: linear-gradient(90deg, #64b5f6, #ce93d8, #81c784);', 'color: #ffffff;')
content = content.replace('-webkit-background-clip: text;', '')
content = content.replace('-webkit-text-fill-color: transparent;', '')

# Monochromatic colors (shades of grey/white/silver)
content = content.replace("'#f44336'", "'#ffffff'")
content = content.replace("'#ff9800'", "'#d0d0d0'")
content = content.replace("'#ffeb3b'", "'#a0a0a0'")
content = content.replace("'#4caf50'", "'#707070'")
content = content.replace("'#2196f3'", "'#505050'")
content = content.replace("'#ce93d8'", "'#303030'")

# Badge colors
content = content.replace('.rank-1 { background: #ffd700; color: #000; }', '.rank-1 { background: #ffffff; color: #000; }')
content = content.replace('.rank-2 { background: #c0c0c0; color: #000; }', '.rank-2 { background: #bbbbbb; color: #000; }')
content = content.replace('.rank-3 { background: #cd7f32; color: #000; }', '.rank-3 { background: #888888; color: #000; }')

# Background
content = content.replace('background: #0a0a1a;', 'background: #000000;')

with open('/root/qm_project/web/index.html', 'w') as f:
    f.write(content)

print("Website updated to monochromatic.")
