# NMOS Transistor: Layout and Model

> **A small training project in chip design.** One NMOS transistor, drawn layer by layer in the
> Magic VLSI editor, plus a simple model of how its current responds to voltage.

![Hand-drawn NMOS layout](figures/nmos_layout.png)

## What it does

Chips are drawn as stacked layers of material. This project covers both sides of a single
transistor:

- **The geometry.** `nmos.mag` is a hand-drawn layout using SCMOS rules: n-diffusion for the
  source and drain, a polysilicon gate crossing the active area, contacts, and metal-1 wiring
  to the source, drain and gate terminals.
- **The behavior.** `nmos_iv.py` is a square-law (Level-1) model with channel-length modulation.
  The width and length come from the drawn layout, and the script plots the transistor's
  current-voltage curves and estimates its threshold voltage.

![Output and transfer characteristics](figures/nmos_iv.png)

## Repository structure

```
nmos-layout-model/
├── nmos.mag            # Magic VLSI layout (open with: magic nmos.mag)
├── render_layout.py    # draws the layout without needing Magic installed
├── nmos_iv.py          # square-law model and I-V plots
└── figures/
```

## Run it

```bash
pip install -r requirements.txt
python render_layout.py   # layout figure
python nmos_iv.py         # I-V curves
```

---

**Author:** Yaşar Aykut Altuntop · MSc student, Biomedical Sciences and Engineering, Koç University  
[LinkedIn](https://linkedin.com/in/aykutaltuntop) · [GitHub](https://github.com/Aykut0)
