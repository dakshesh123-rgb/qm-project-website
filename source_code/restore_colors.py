import re

with open('/root/qm_project/web/index.html', 'r') as f:
    content = f.read()

# Restore colors
content = content.replace("'#ffffff'", "'#f44336'")
content = content.replace("'#d0d0d0'", "'#ff9800'")
content = content.replace("'#a0a0a0'", "'#ffeb3b'")
content = content.replace("'#707070'", "'#4caf50'")
content = content.replace("'#505050'", "'#2196f3'")
content = content.replace("'#303030'", "'#ce93d8'")

content = content.replace('.rank-1 { background: #ffffff; color: #000; }', '.rank-1 { background: #ffd700; color: #000; }')
content = content.replace('.rank-2 { background: #bbbbbb; color: #000; }', '.rank-2 { background: #c0c0c0; color: #000; }')
content = content.replace('.rank-3 { background: #888888; color: #000; }', '.rank-3 { background: #cd7f32; color: #000; }')

content = content.replace('background: #000000;', 'background: #0a0a1a;')

# Restore gradient text in header
content = re.sub(r'color: #ffffff;\s*margin-bottom: 6px;', 
    r'background: linear-gradient(90deg, #64b5f6, #ce93d8, #81c784);\n            -webkit-background-clip: text;\n            -webkit-text-fill-color: transparent;\n            margin-bottom: 6px;', content)

with open('/root/qm_project/web/index.html', 'w') as f:
    f.write(content)

print("Colors restored!")
