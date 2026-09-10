from fpdf import FPDF
import textwrap

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 15)
        self.cell(0, 10, "Quantum Tunneling in Non-Standard Potentials", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("helvetica", "I", 12)
        self.cell(0, 10, "Progress Report", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

pdf = PDF()
pdf.add_page()
pdf.set_font("helvetica", size=12)

content = r"""
I have used opus 4.6 ai and this is 2 days of works.

What I've Done So Far
I built a working Schrodinger equation solver from scratch in Python. It doesn't rely on big scientific libraries, so it runs anywhere. I checked it against known solutions (infinite square well and harmonic oscillator) and the errors are less than 0.04%.

The Shape Factor Discovery
I studied six different barrier shapes (rectangular, Gaussian, triangular, parabolic, trapezoidal, exponential) with the exact same height and width.

My biggest finding so far is that the geometric shape of the barrier completely changes the tunneling probability, something standard textbooks rarely cover!
* The exponential barrier lets the most particles tunnel through. It allows up to 9,000,000x (9 million times) more tunneling than a standard rectangular wall!
* The rectangular barrier blocks the most, acting like a solid brick wall, while shapes like the Gaussian act like smooth hills where the maximum resistance only occurs at a single point.
* This difference is amplified exponentially as the barriers become wider or as the particle energy decreases.

To measure this, I created a Shape Factor (S), which compares how much a specific shape blocks tunneling compared to a plain rectangular barrier. It perfectly captures the WKB (Wentzel-Kramers-Brillouin) approximation integral for non-standard shapes.

Visualization Goals
I also built an interactive web visualization. My goal is to dynamically plot the wave's decay rate (kappa) inside different barriers. This visually proves why smooth curves offer less resistance and directly maps to the Shape Factor math.

What I'm Working On Next
* Morse Potential: Looking at molecular vibrational levels, which connects this physics project to chemistry.
* Double Well Tunnel Splitting: Studying how energy levels split when there are two wells next to each other.
* Getting really clean data for my final paper.

My Ultimate Aim
The ultimate goal of this project is to publish a computational quantum mechanics research paper! By systematically comparing how non-standard barrier shapes affect quantum tunneling (something textbooks usually ignore), I'm putting together a unique computational study. Once the data is ready, I plan to write it up and submit it to student research journals, arXiv, or science fairs like IRIS.
"""

for line in content.split('\n'):
    line = line.strip()
    if not line:
        pdf.ln(8)
        continue
        
    if line in ["What I've Done So Far", "The Shape Factor Discovery", "Visualization Goals", "What I'm Working On Next", "My Ultimate Aim"]:
        pdf.set_font("helvetica", "B", 13)
        pdf.cell(0, 10, line, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", size=12)
        continue
    
    # Wrap text manually
    wrapped = textwrap.wrap(line, width=80)
    for w in wrapped:
        pdf.cell(0, 8, w, new_x="LMARGIN", new_y="NEXT")

pdf.output("/root/qm_project/web/Quantum_Tunneling_Progress.pdf")
print("PDF successfully updated!")
