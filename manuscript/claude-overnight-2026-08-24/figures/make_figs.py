import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SURF="#fcfcfb"; INK="#0b0b0b"; INK2="#52514e"; MUTED="#8a8985"; GRID="#e4e3df"
BLUE="#2a78d6"; ORANGE="#eb6834"; AQUA="#1baf7a"; VIOLET="#4a3aa7"

# ---------------- Figure 1 ----------------
fam = ["grid2d","grid3d","double_cycle","binary_tree","caterpillar","comb",
       "spider","star","decoy_hub","rand_reg3","rand_reg4","rrt"]
amg  = [0.26,-0.14,0.16,-0.00,0.26,0.17,0.17,-0.00,0.18,-0.16,0.01,-0.16]
push = [0.83,0.82,0.94,0.96,0.95,0.97,0.94,1.00,0.95,1.08,1.11,0.99]
cheb = [0.83,0.46,0.63,0.29,0.74,0.75,0.65,0.80,0.64,0.28,0.60,0.50]
direct=[0.79,0.36,0.08,-0.21,0.01,0.04,0.09,-0.00,-0.00,None,None,None]

fig = plt.figure(figsize=(10.0,7.4), dpi=170)
fig.patch.set_facecolor(SURF)
ax = fig.add_axes([0.145,0.115,0.825,0.665]); ax.set_facecolor(SURF)
y = np.arange(len(fam))[::-1]

ax.axvspan(-0.32,0.35, color=AQUA, alpha=0.055, lw=0, zorder=0)
ax.axvline(0.0, color=INK2, lw=1.0, ls=(0,(4,3)), alpha=0.55, zorder=1)
ax.axvline(1.0, color=INK2, lw=1.0, ls=(0,(4,3)), alpha=0.55, zorder=1)
for yi in y: ax.plot([-0.32,1.22],[yi,yi], color=GRID, lw=0.7, zorder=1)

for name,vals,col,mk in [("push",push,ORANGE,"o"),
                         ("Chebyshev (truncated)",cheb,VIOLET,"^"),
                         ("elimination (direct)",direct,BLUE,"s"),
                         ("local AMG",amg,AQUA,"D")]:
    xs=[v for v in vals if v is not None]; ys=[yi for v,yi in zip(vals,y) if v is not None]
    ax.scatter(xs,ys,s=66,c=col,marker=mk,zorder=4,label=name,
               edgecolors=SURF,linewidths=1.6)

ax.set_yticks(y); ax.set_yticklabels(fam, fontsize=10.5, color=INK)
ax.set_xlim(-0.32,1.22); ax.set_ylim(-0.75, len(fam)-0.25)
ax.set_xticks([0,0.25,0.5,0.75,1.0]); ax.tick_params(axis="x", colors=INK2, labelsize=10)
ax.tick_params(axis="y", length=0)
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.set_xlabel("fitted exponent  s   in   W / vol(S$_\\varepsilon$)  ~  α$^{-s}$",
              fontsize=11, color=INK2, labelpad=10)
ax.text(0.015, -0.62, "α-free band", fontsize=9.2, color="#12805a", va="center")
ax.text(0.985, -0.62, "≈ 1/α  (APPR baseline)", fontsize=9.2, color=INK2, va="center", ha="right")

fig.text(0.045,0.945,"Which local PPR mechanisms are α-free?",
         fontsize=16, color=INK, fontweight="600", va="top")
fig.text(0.045,0.898,
  "s ≈ 0 means charged work per unit of output does not grow as the teleportation parameter shrinks.\n"
  "12 graph families · α ∈ {2⁻⁴, 2⁻⁸, 2⁻¹²} · ε = 10⁻⁶ · every run certified against the exact solve.",
  fontsize=10, color=INK2, va="top", linespacing=1.55)
h,l = ax.get_legend_handles_labels()
leg = fig.legend(h,l, loc="upper left", bbox_to_anchor=(0.043,0.822), ncol=4,
                 frameon=False, fontsize=10, handletextpad=0.35, columnspacing=1.9)
for t in leg.get_texts(): t.set_color(INK2)
fig.text(0.97,0.012,"elimination not run on expanders / heavy-tailed trees (catastrophic fill)",
         fontsize=8.6, color=MUTED, ha="right")
fig.savefig("/home/claude/work/overnight/figures/fig1_alpha_exponents.png", facecolor=SURF)
plt.close(fig)

# ---------------- Figure 2 ----------------
labels = ["α = 2⁻¹⁰\nhub degree 48\n|∂S| = 2,880",
          "α = 2⁻¹⁰\nhub degree 384\n|∂S| = 23,040",
          "α = 2⁻¹²\nhub degree 384\n|∂S| = 23,040"]
pull=[129780,1705140,2465460]; pushg=[5764,9247,13211]; kin=[4156,5899,9253]

fig = plt.figure(figsize=(9.2,6.2), dpi=170); fig.patch.set_facecolor(SURF)
ax = fig.add_axes([0.115,0.155,0.86,0.60]); ax.set_facecolor(SURF)
x=np.arange(3); w=0.24
for name,vals,col,off in [("rescan the boundary (pull)",pull,ORANGE,-w),
                          ("pushed accumulators",pushg,BLUE,0.0),
                          ("kinetic event queue",kin,AQUA,w)]:
    ax.bar(x+off, vals, width=w-0.024, color=col, label=name, zorder=3,
           edgecolor=SURF, linewidth=1.4)
    for xi,v in zip(x+off, vals):
        ax.text(xi, v*1.16, f"{v:,}", ha="center", fontsize=8.8, color=INK2, zorder=4)

ax.set_yscale("log"); ax.set_ylim(1.8e3, 6e6)
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=9.5, color=INK2, linespacing=1.6)
ax.grid(axis="y", color=GRID, lw=0.7, zorder=0); ax.set_axisbelow(True)
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(axis="y", colors=INK2, labelsize=9.5); ax.tick_params(axis="y", which="minor", length=0); ax.tick_params(axis="x", length=0)
ax.set_ylabel("charged gate work (log scale)", fontsize=10.5, color=INK2, labelpad=8)
ax.annotate("", xy=(2+w, 9253*2.1), xytext=(2-w, 2465460*0.5),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2,
                            connectionstyle="arc3,rad=-0.25"), zorder=5)
ax.text(2.30, 1.1e5, "266×", fontsize=14, color=INK, fontweight="600", ha="center")

fig.text(0.045,0.945,"The boundary scan was an accounting artifact",
         fontsize=16, color=INK, fontweight="600", va="top")
fig.text(0.045,0.898,
  "On a marginal-hub ring, 87% of a local solver's charged work was rescanning the boundary for gate violations.\n"
  "Pushing two accumulators inside the interior solver's own scans reports every violation exactly — 0 misses, 0 false reports.",
  fontsize=10, color=INK2, va="top", linespacing=1.55)
h,l = ax.get_legend_handles_labels()
leg = fig.legend(h,l, loc="upper left", bbox_to_anchor=(0.043,0.815), ncol=3,
                 frameon=False, fontsize=9.8, handletextpad=0.45, columnspacing=1.9)
for t in leg.get_texts(): t.set_color(INK2)
fig.savefig("/home/claude/work/overnight/figures/fig2_boundary_gate.png", facecolor=SURF)
print("ok")
