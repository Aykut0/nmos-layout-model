"""
NMOS I-V characterization
=========================
Level-1 (square-law) MOSFET model with channel-length modulation, matching the
NMOS device laid out in nmos.mag. Produces the two textbook characterization plots:

  * output characteristics  Id vs Vds for a family of Vgs
  * transfer characteristic Id vs Vgs (with sqrt(Id) for Vt extraction)

    python nmos_iv.py   ->   figures/nmos_iv.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")

# device / process parameters (typical 0.5 um SCMOS NMOS)
VT = 0.7          # threshold voltage [V]
KP = 120e-6       # transconductance parameter mu*Cox [A/V^2]
W, L = 4.0, 2.0   # from layout: gate 8 lambda wide, channel 2 lambda long -> W/L=4
LAMBDA = 0.04     # channel-length modulation [1/V]
K = KP * W / L


def id_nmos(vgs, vds):
    vov = vgs - VT
    if vov <= 0:
        return 0.0
    if vds < vov:  # triode / linear
        return K * (vov * vds - 0.5 * vds ** 2) * (1 + LAMBDA * vds)
    return 0.5 * K * vov ** 2 * (1 + LAMBDA * vds)  # saturation


def main():
    os.makedirs(FIG, exist_ok=True)
    vds = np.linspace(0, 3.3, 400)
    vgs_family = [1.0, 1.5, 2.0, 2.5, 3.0]

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))

    # output characteristics
    for vgs in vgs_family:
        idc = np.array([id_nmos(vgs, v) for v in vds]) * 1e6
        ax[0].plot(vds, idc, lw=1.6, label=f"Vgs = {vgs:.1f} V")
        vov = vgs - VT
        if vov > 0:
            ax[0].plot(vov, id_nmos(vgs, vov) * 1e6, "k.", ms=6)
    ax[0].set_xlabel("Vds [V]"); ax[0].set_ylabel("Id [µA]")
    ax[0].set_title("Output characteristics (Id–Vds)\ndots = triode/saturation boundary")
    ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3)

    # transfer characteristic at fixed Vds (saturation)
    vgs = np.linspace(0, 3.3, 400)
    idsat = np.array([id_nmos(g, 3.0) for g in vgs])
    ax[1].plot(vgs, idsat * 1e6, color="#2563eb", lw=1.8, label="Id")
    ax[1].set_xlabel("Vgs [V]"); ax[1].set_ylabel("Id [µA]", color="#2563eb")
    ax[1].tick_params(axis="y", labelcolor="#2563eb")
    ax[1].set_title("Transfer characteristic (Id–Vgs, Vds = 3 V)")
    ax[1].grid(alpha=0.3)
    axr = ax[1].twinx()
    axr.plot(vgs, np.sqrt(idsat), color="#dc2626", lw=1.5, ls="--", label="√Id")
    axr.set_ylabel("√Id  [√A]", color="#dc2626")
    axr.tick_params(axis="y", labelcolor="#dc2626")
    axr.axvline(VT, color="#6b7280", ls=":", lw=1)
    axr.annotate(f"Vt = {VT} V", (VT, 0), xytext=(VT + 0.15, 0.0005),
                 fontsize=9, color="#374151")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "nmos_iv.png"), dpi=140)
    plt.close(fig)
    print("wrote figures/nmos_iv.png")


if __name__ == "__main__":
    main()
