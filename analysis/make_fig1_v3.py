"""Figure 1, second design: asset and records (with a real C-MAPSS sensor trajectory and a schematic engine), the two routes with data thumbnails,
and the evaluation design with one headline outcome. All values plotted come from the data or from summary_upgrade1.json."""
import json, os, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle
B = str(__import__('pathlib').Path(__file__).resolve().parents[1]); S = json.load(open(B + '/upgrade1/summary_upgrade1.json'))
RAW = os.environ.get('CMAPSS_DIR', 'data/cmapss')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 6.5})
GREY, BLUE, ORANGE, INK, LIGHT, HEAD = '#7d7d78', '#2a78d6', '#eb6834', '#2b2b29', '#d9d9d4', '#4a4f57'
a = np.loadtxt(f'{RAW}/train_FD001.txt'); e = a[a[:, 0] == 2]; y = e[-110:, 4 + 11]; y = (y - y.min()) / (y.max() - y.min()); T = len(y); t = np.arange(T)
rng = np.random.default_rng(1); irr = [T - 1]
for g in rng.integers(1, 6, 60):
    if irr[-1] - g < 0: break
    irr.append(irr[-1] - g)
irr = np.array(irr[::-1]); k5 = t[::-1][::5][::-1]
fig = plt.figure(figsize=(7.4, 4.9)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 148); ax.set_ylim(0, 98); ax.axis('off')
def panel(x0, y0, w, h, title):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle='round,pad=0,rounding_size=1.6', fc='#fbfbf9', ec=HEAD, lw=0.9))
    ax.add_patch(FancyBboxPatch((x0, y0 + h - 4.4), w, 4.4, boxstyle='round,pad=0,rounding_size=1.6', fc=HEAD, ec=HEAD, lw=0.9))
    ax.add_patch(Rectangle((x0, y0 + h - 4.4), w, 2.2, fc=HEAD, ec='none'))
    ax.text(x0 + 2, y0 + h - 2.2, title, color='white', fontsize=7.0, fontweight='bold', va='center')
def box(x0, y0, w, h, text, col, fs=5.9, bold=False, tx=None, ha='center'):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle='round,pad=0,rounding_size=1.2', fc='white', ec=col, lw=0.9))
    ax.text(x0 + w / 2 if tx is None else tx, y0 + h / 2, text, ha=ha, va='center', fontsize=fs, color=INK, fontweight='bold' if bold else 'normal', linespacing=1.15)
def arrow(p, q, col): ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>', color=col, lw=1.0, shrinkA=0, shrinkB=0, mutation_scale=7))
def thumb(x0, y0, w, h, idx, col, line=None, title=None, full=True, frame=True):
    ia = ax.inset_axes([x0, y0, w, h], transform=ax.transData); ia.set_xlim(-3, T + 2); ia.set_ylim(-0.12, 1.15)
    if full: ia.plot(t, y, color=LIGHT, lw=0.7)
    if line is not None: ia.plot(line[0], line[1], color=col, lw=0.9)
    ia.scatter(idx, y[idx], s=3.0, color=col, zorder=3, linewidths=0); ia.set_xticks([]); ia.set_yticks([]); ia.patch.set_alpha(1.0 if frame else 0.0)
    for sp in ia.spines.values(): sp.set_color('#c8c8c2'); sp.set_linewidth(0.5); sp.set_visible(frame)
    if title: ia.set_title(title, fontsize=5.6, pad=1.5, color=INK)

# ================= (a) asset and records =================
panel(1, 70.5, 146, 26.5, '(a)  Monitored asset and what is recorded')
cx0, cy, sc = 5, 82.3, 0.62; mods = [('Fan', 9, 8.5, 6.2), ('LPC', 6, 6.0, 5.0), ('HPC', 9, 5.0, 3.0), ('Comb.', 6, 3.4, 3.4), ('HPT', 5, 3.2, 4.2), ('LPT', 8, 4.2, 6.0), ('Nozzle', 6, 5.6, 3.8)]
x = cx0
for name, w, h0, h1 in mods:
    for sgn in (1, -1):
        ax.add_patch(Polygon([(x, cy + sgn * 0.5), (x, cy + sgn * h0 * sc), (x + w, cy + sgn * h1 * sc), (x + w, cy + sgn * 0.5)], closed=True, fc='#e9eef5' if name != 'Comb.' else '#fbe6da', ec='#6b7a8f', lw=0.6))
    ax.text(x + w / 2, cy - 6.6, name, ha='center', va='center', fontsize=5.0, color=INK); x += w + 0.6
ax.plot([cx0, x - 0.6], [cy, cy], color='#6b7a8f', lw=0.8)
for sx in (cx0 + 10.5, cx0 + 17, cx0 + 27, cx0 + 39.5, cx0 + 49): ax.plot(sx, cy + 6.3, marker='v', ms=3, color=ORANGE, mec='none')
ax.text(cx0 + 27, cy + 8.3, 'temperature, pressure and speed sensors', ha='center', va='center', fontsize=5.2, color=ORANGE)
ax.text(cx0 + 27, 72.6, 'turbofan engine, simulated run to failure (C-MAPSS, N-CMAPSS); schematic', ha='center', va='center', fontsize=5.2, color='#555')
w_, h_, yb = 19.3, 12.6, 75.3
for x0, idx, col, ttl, full in ((62, t, GREY, 'complete: every cycle', False), (83.6, k5, BLUE, 'sparse: every 5th cycle', True), (105.2, irr, BLUE, 'irregular gaps', True), (126.8, t[-10:], ORANGE, 'short history', True)):
    thumb(x0, yb, w_, h_, idx, col, title=ttl, full=full)
ax.text(104, 72.6, 'one sensor of one C-MAPSS engine, last 110 cycles; each window ends at the prediction time', ha='center', va='center', fontsize=5.2, color='#555')

# ================= (b) two routes =================
panel(1, 1.5, 98, 66.5, '(b)  Two ways to handle sparse records')
bh = 8.6
def lane(y0, h, col, fill, title, mid_tr, mid_dp, tr_idx, tr_line, dp_line, bold_tr):
    ax.add_patch(FancyBboxPatch((3, y0), 94, h, boxstyle='round,pad=0,rounding_size=1.4', fc=fill, ec='none'))
    ax.text(5, y0 + h - 2.5, title, fontsize=6.8, color=col, fontweight='bold', va='center')
    yt, yd = y0 + h - 5.0 - bh, y0 + 1.6
    for yy, lab in ((yt, 'training'), (yd, 'in service')): ax.text(5.4, yy + bh / 2, lab, fontsize=5.2, color='#666', rotation=90, va='center', ha='center')
    thumb(8, yt, 19, bh, tr_idx, col, line=tr_line); thumb(8, yd, 19, bh, k5, col)
    box(33, yt, 30, bh, mid_tr, col, bold=bold_tr)
    if dp_line is None: box(33, yd, 30, bh, mid_dp, col, bold=not bold_tr)
    else:
        box(33, yd, 30, bh, mid_dp, col, bold=not bold_tr, tx=45.2, ha='left', fs=5.6); thumb(33.7, yd + 0.7, 10.8, bh - 1.4, k5, col, line=dp_line, full=False, frame=False)
    box(69, yt, 26, bh, 'fit predictor\n(GRU, TCN or Transformer)', col, fs=5.5); box(69, yd, 26, bh, 'predictor  →  RUL', col)
    for yy in (yt, yd): arrow((27.6, yy + bh / 2), (32.4, yy + bh / 2), col); arrow((63.6, yy + bh / 2), (68.4, yy + bh / 2), col)
    arrow((82, yt - 0.4), (82, yd + bh + 0.4), col)
interp = (np.arange(k5[0], T), np.interp(np.arange(k5[0], T), k5, y[k5]))
lane(34.0, 28.2, GREY, '#f0f0ed', 'Test-time repair (reference)', 'windows of\nconsecutive cycles', 'repair to every\ncycle: interpolate,\ncarry forward\nor impute', t[-30:], (t[-30:], y[-30:]), interp, False)
lane(3.6, 28.2, BLUE, '#e9f1fc', 'Sparsified-window training (SWT)', 'records deleted at random;\nRUL target at the window\nend unchanged', 'used as recorded, plus time\ngaps: gap channel (A5) or\nevery-cycle grid (A8)', irr[-30:], None, None, True)

# ================= (c) evaluation =================
panel(101, 1.5, 46, 66.5, '(c)  What the evaluation tests')
items = [('Source of the gain', 'GRU controls for history\nspan and padding', BLUE), ('External cohort', 'N-CMAPSS DS03–DS08,\nfixed split and models', BLUE), ('Other backbones', 'TCN, Transformer; each\narm tuned separately', BLUE),
         ('Unseen missingness', 'block outages,\nregime-dependent gaps', BLUE), ('Limits', 'cost with complete records;\nshort histories (boundary)', ORANGE)]
yy = 61.6
for head, txt, col in items:
    ax.add_patch(FancyBboxPatch((103, yy - 8.6), 42, 8.5, boxstyle='round,pad=0,rounding_size=1.1', fc='white', ec=col, lw=0.8))
    ax.text(104.5, yy - 2.1, head, fontsize=6.0, fontweight='bold', color=col, va='center'); ax.text(104.5, yy - 5.9, txt, fontsize=5.2, color=INK, va='center', linespacing=1.1); yy -= 9.5
v0, v1 = S['ext|k5|A1'], S['ext|k5|A5']; bx, by = 104.5, 3.6
ax.text(103, 12.4, 'External cohort, every 5th cycle (RMSE, cycles)', fontsize=5.2, color='#555', va='center')
for i, (v, col, lab) in enumerate(((v0, GREY, 'best repair'), (v1, BLUE, 'SWT'))):
    y0 = by + 3.7 * (1 - i); ax.add_patch(Rectangle((bx + 11, y0), v * 1.5, 2.6, fc=col, ec='none'))
    ax.text(bx + 10.3, y0 + 1.3, lab, ha='right', va='center', fontsize=5.3, color=INK); ax.text(bx + 11 + v * 1.5 + 0.8, y0 + 1.3, f'{v:.1f}', va='center', fontsize=5.6, color=INK, fontweight='bold')
fig.savefig(B + '/figures/fig1_overview_v3.png', dpi=300, bbox_inches='tight', pad_inches=0.02); fig.savefig(B + '/figures/fig1_overview_v3.pdf', bbox_inches='tight', pad_inches=0.02); print('ok', round(v0, 2), round(v1, 2))
