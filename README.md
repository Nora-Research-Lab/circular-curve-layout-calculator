![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Circular Curve Layout Calculator
 
*For surveyors and civil engineers: enter intersection angle, radius, and PI station to instantly compute all horizontal circular curve elements and get a printable layout table.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Surveying & Mapping
 
This tool computes the full geometric layout of a horizontal circular curve, a standard task in route surveying. 

Inputs (user provides):
- Intersection angle (Δ) in decimal degrees (0 < Δ < 180)
- Radius (R) in meters or feet (user chooses unit via a dropdown)
- Station of the Point of Intersection (PI) in the format 'XX+YY.ZZ' (e.g., '12+45.67' meaning 1245.67 units from datum)
- (Optional) Station interval for layout points (default 10 m or 25 ft based on unit choice)

Core calculation logic (step by step):
1. Convert Δ to radians: Δ_rad = Δ × π/180.
2. Tangent length T = R × tan(Δ_rad/2).
3. Curve length L = R × Δ_rad (in same units as R).
4. Chord length C = 2 × R × sin(Δ_rad/2).
5. External distance E = R × (1/cos(Δ_rad/2) - 1).
6. Mid-ordinate M = R × (1 - cos(Δ_rad/2)).
7. Station of Point of Curvature (PC) = PI station - T.
8. Station of Point of Tangency (PT) = PC station + L.
9. For layout at user-chosen interval (s), generate station values from PC to PT at steps of s. For each intermediate station i, compute: deflection angle from PC = (station i - PC) * (Δ_rad / L) * (180/π) / 2, and chord distance from PC = 2 × R × sin( (station i - PC) * (Δ_rad / L) / 2 ).

UI layout:
- Top section: a centered title, one-line pitch, and an image banner (placeholder).
- Left column: input fields. For Δ: number input (0-180). For R: number input (positive). Unit dropdown: [meters, feet]. For PI station: text input with placeholder 'XX+YY.ZZ'. For interval: number input with default based on unit.
- Right column: output elements — a text summary showing T, L, C, E, M, PC station, PT station (with units), then a scrollable HTML table showing the layout stations with their deflection angle (in degrees) and chord distance. Additionally, a 'Download as CSV' button for the layout table.
- No AI/ML component; purely geometric formulas and a simple unit conversion.

All outputs display with 2 decimal places, and stations are formatted as 'XX+YY.ZZ'.
 
## Run it
 
```bash
docker build -t circular-curve-layout-calculator .
docker run -p 7860:7860 circular-curve-layout-calculator
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-25.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
