"""
Render the Magic NMOS layout (nmos.mag) as a labelled layer diagram.

Parses the SCMOS `.mag` rectangles and draws each layer with conventional colours
(ndiffusion green, polysilicon red, contacts, metal1 blue) so the layout is viewable
without opening the Magic VLSI tool.

    python render_layout.py   ->   figures/nmos_layout.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")

STYLE = {  # (facecolor, alpha, hatch, z)
    "ndiffusion":  ("#22c55e", 0.55, "",   1),
    "polysilicon": ("#ef4444", 0.55, "",   2),
    "ndcontact":   ("#1f2937", 0.80, "xx", 3),
    "polycontact": ("#1f2937", 0.80, "xx", 3),
    "metal1":      ("#3b82f6", 0.35, "//", 4),
}


def parse_mag(path):
    layer, out = None, []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("<<") and line.endswith(">>"):
                layer = line.strip("<> ").strip()
            elif line.startswith("rect") and layer in STYLE:
                _, x0, y0, x1, y1 = line.split()
                out.append((layer, int(x0), int(y0), int(x1), int(y1)))
            elif line.startswith("rlabel"):
                p = line.split()
                out.append(("_label", int(p[2]), int(p[3]), p[-1]))
    return out


def main():
    os.makedirs(FIG, exist_ok=True)
    items = parse_mag(os.path.join(HERE, "nmos.mag"))
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    for it in items:
        if it[0] == "_label":
            _, x, y, name = it
            ax.text(x, y, name, ha="center", va="center", fontsize=12,
                    fontweight="bold", color="white",
                    bbox=dict(boxstyle="circle", fc="#111827", ec="none"))
            continue
        layer, x0, y0, x1, y1 = it
        fc, al, hatch, z = STYLE[layer]
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=fc, alpha=al,
                               edgecolor=fc, hatch=hatch, zorder=z, lw=1.2))
    ax.set_xlim(-10, 50); ax.set_ylim(-12, 46); ax.set_aspect("equal")
    ax.set_xlabel("x [λ]"); ax.set_ylabel("y [λ]")
    ax.set_title("NMOS transistor — SCMOS layout (Magic)")
    legend = [Patch(facecolor=STYLE[k][0], alpha=max(STYLE[k][1], 0.5),
                    hatch=STYLE[k][2], label=k) for k in STYLE]
    ax.legend(handles=legend, loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=9)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "nmos_layout.png"), dpi=140)
    plt.close(fig)
    print("wrote figures/nmos_layout.png")


if __name__ == "__main__":
    main()
