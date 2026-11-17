"""v19 figures: Figure 1 (overview of DMWT and its evaluation), Figure 6 (external cohort), Figure 7 (padding experiment)."""
import json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B = str(__import__('pathlib').Path(__file__).resolve().parents[1]); S = json.load(open(B + '/upgrade1/summary_upgrade1.json'))
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 7, 'axes.linewidth': 0.6, 'axes.edgecolor': '#555', 'xtick.color': '#555',
                     'ytick.color': '#555', 'axes.spines.top': False, 'axes.spines.right': False, 'legend.frameon': False})
GREY, BLUE, ORANGE, INK = '#8a8a85', '#2a78d6', '#eb6834', '#2b2b29'
def save(fig, n): fig.savefig(f'{B}/figures/{n}.png', dpi=300, bbox_inches='tight'); fig.savefig(f'{B}/figures/{n}.pdf', bbox_inches='tight'); plt.close(fig)

# ======================= Figure 1 =======================
fig = plt.figure(figsize=(7.4, 3.9)); gs = fig.add_gridspec(1, 3, width_ratios=[0.9, 2.45, 1.25], wspace=0.05)
# ---- (a) observation problem ----
ga = gs[0].subgridspec(5, 1, hspace=0.6, height_ratios=[0.08, 1, 1, 1, 1]); rng = np.random.default_rng(3); T = 60; t = np.arange(T); x = 0.15 * np.exp(t / 26) + rng.normal(0, 0.04, T)
irr = [T - 1]
for g in rng.integers(1, 6, 40):
    if irr[-1] - g < 0: break
    irr.append(irr[-1] - g)
rows = [('Complete: every cycle', t, GREY), ('Sparse: every fifth cycle', t[::-1][::5], BLUE), ('Irregular gaps', np.array(irr), BLUE), ('Short history: last cycles', t[-8:], ORANGE)]
for i, (lab, idx, col) in enumerate(rows):
    ax = fig.add_subplot(ga[i + 1]); ax.plot(t, x, color='#d5d5d0', lw=0.8); ax.scatter(idx, x[idx], s=5, color=col, zorder=3)
    ax.axvline(T - 1, color=INK, lw=0.6, ls=':'); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(lab, fontsize=6.5, loc='left', pad=2)
    for sp in ('left', 'bottom'): ax.spines[sp].set_color('#bbb')
    if i == 0: ax.text(T - 3, x.min(), 'prediction time', fontsize=5.2, ha='right', va='bottom', color=INK)
    if i == 3: ax.set_xlabel('operating cycles', fontsize=6)
fig.text(0.125, 0.889, '(a) What is recorded', fontsize=7.2, fontweight='bold', va='bottom')
# ---- (b) two routes ----
ax = fig.add_subplot(gs[1]); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
def box(ax, x0, y0, w, h, text, col, fill='white', fs=5.7, bold=False):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle='round,pad=0.3,rounding_size=1.5', fc=fill, ec=col, lw=0.9))
    ax.text(x0 + w / 2, y0 + h / 2, text, ha='center', va='center', fontsize=fs, color=INK, fontweight='bold' if bold else 'normal', linespacing=1.15)
def arrow(ax, a, b, col): ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=col, lw=0.9, shrinkA=0, shrinkB=0, mutation_scale=7))
ax.text(3, 101, '(b) Two ways to handle sparse records', fontsize=7.2, fontweight='bold', va='bottom')
# lane backgrounds
ax.add_patch(FancyBboxPatch((3, 51), 95, 39, boxstyle='round,pad=0.2,rounding_size=2', fc='#f5f5f3', ec='none'))
ax.add_patch(FancyBboxPatch((3, 3), 95, 44, boxstyle='round,pad=0.2,rounding_size=2', fc='#eef4fc', ec='none'))
ax.text(5, 87.5, 'Test-time repair (reference)', fontsize=6.8, color=GREY, fontweight='bold', va='center')
ax.text(5, 44.3, 'Deployment-matched window training (DMWT)', fontsize=6.8, color=BLUE, fontweight='bold', va='center')
for y_tr, y_dp, col, mid_tr, mid_dp in ((72, 55, GREY, 'windows of\nconsecutive cycles', 'repair to every cycle:\ninterpolate, carry\nforward or impute'),
                                        (27, 7, BLUE, 'windows sparsified\nat random; RUL target\nunchanged', 'used as recorded, plus\ntime gaps: gap channel\n(A5) or cycle grid (A8)')):
    h = 11 if col == GREY else 12.5
    ax.text(5.5, y_tr + h / 2, 'training', fontsize=5.4, color='#666', rotation=90, va='center', ha='center'); ax.text(5.5, y_dp + h / 2, 'in service', fontsize=5.4, color='#666', rotation=90, va='center', ha='center')
    box(ax, 9, y_tr, 21, h, 'run-to-failure\nrecords', col); box(ax, 36, y_tr, 35, h, mid_tr, col, bold=(col == BLUE)); box(ax, 77, y_tr, 19, h, 'fit\npredictor', col)
    box(ax, 9, y_dp, 21, h, 'sparse\nrecords', col); box(ax, 36, y_dp, 35, h, mid_dp, col, bold=(col == GREY)); box(ax, 77, y_dp, 19, h, 'predictor\n→ RUL', col)
    for yy in (y_tr, y_dp): arrow(ax, (30.8, yy + h / 2), (35.2, yy + h / 2), col); arrow(ax, (71.8, yy + h / 2), (76.2, yy + h / 2), col)
    arrow(ax, (86.5, y_tr - 0.8), (86.5, y_dp + h + 0.8), col)
# ---- (c) evaluation design ----
ax = fig.add_subplot(gs[2]); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
ax.text(3, 101, '(c) What the evaluation tests', fontsize=7.2, fontweight='bold', va='bottom')
items = [('Source of the gain', 'GRU controls: history span\nand padding (A8F, A6S)', BLUE), ('External cohort', 'N-CMAPSS DS03–DS08,\nfixed split and models', BLUE),
         ('Other backbones', 'TCN, Transformer; each\narm tuned separately', BLUE), ('Unseen missingness', 'block outages,\nregime-dependent gaps', BLUE),
         ('Limits', 'cost with complete records;\nshort histories (boundary case)', ORANGE)]
y = 88
for head, txt, col in items:
    ax.add_patch(FancyBboxPatch((3, y - 15), 94, 14.5, boxstyle='round,pad=0.3,rounding_size=1.5', fc='white', ec=col, lw=0.9))
    ax.text(6, y - 3.4, head, fontsize=6.4, fontweight='bold', color=col, va='center'); ax.text(6, y - 9.9, txt, fontsize=5.8, color=INK, va='center', linespacing=1.15); y -= 17.4
save(fig, 'fig1_overview')

# ======================= Figure 6: external cohort =======================
fig, axs = plt.subplots(1, 2, figsize=(7.4, 2.6), gridspec_kw={'width_ratios': [1.55, 1]})
def bars(ax, scs, labs, arms, cols, names):
    w = 0.8 / len(arms)
    for j, (a, c, n) in enumerate(zip(arms, cols, names)):
        ax.bar(np.arange(len(scs)) + j * w - 0.4 + w / 2, [S[f'ext|{sc}|{a}'] for sc in scs], w, color=c, label=n)
    ax.set_xticks(range(len(scs))); ax.set_xticklabels(labs, fontsize=6.5); ax.yaxis.grid(True, lw=0.3, color='#ddd'); ax.set_axisbelow(True); ax.set_ylim(0, 27)
bars(axs[0], ['k1', 'k5', 'irr5', 'blk5', 'blk10'], ['every cycle', 'every 5th', 'irregular 1–5', 'block 5 *', 'block 10 *'], ['A1', 'A2', 'A5', 'A8'],
     [GREY, '#b5b5ae', BLUE, ORANGE], ['dense, raw input (A1)', 'dense + interpolation (A2)', 'DMWT, gap channel (A5)', 'DMWT, long input (A8)'])
axs[0].set_title('(a) Sparse records', fontsize=7.5); axs[0].set_ylabel('RMSE (cycles)'); axs[0].legend(fontsize=5.8, ncol=2, loc='upper left')
bars(axs[1], ['full', 'h5', 'h3'], ['complete', 'last 5', 'last 3'], ['S1', 'S2', 'S4', 'S8'], [GREY, '#b5b5ae', BLUE, ORANGE],
     ['dense, repeat padding (S1)', 'dense, zero padding (S2)', 'DMWT, truncation (S4)', 'DMWT, long input (S8)'])
axs[1].set_title('(b) Short histories', fontsize=7.5); axs[1].legend(fontsize=5.8, ncol=1, loc='upper left'); axs[1].set_ylim(0, 34)
fig.tight_layout(); save(fig, 'fig6_external')

# ======================= Figure 7: padding experiment =======================
fig, axs = plt.subplots(1, 2, figsize=(7.4, 2.5), gridspec_kw={'width_ratios': [1, 1.7]})
ax = axs[0]; ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off'); ax.set_title('(a) Which training windows are truncated', fontsize=7.5)
arms = [('S1', 'none', []), ('S3E', 'high RUL only', [(22, 60)]), ('S3', 'all', [(22, 96)]), ('S3L', 'low RUL only', [(60, 96)])]
cols = {'S1': GREY, 'S3E': '#9a6324', 'S3': '#b07ccf', 'S3L': '#1baf7a'}
for i, (a, lab, seg) in enumerate(arms):
    y = 78 - i * 19; ax.text(1, y + 4, a, fontsize=6.6, fontweight='bold', color=cols[a], va='center'); ax.text(1, y - 3.2, lab, fontsize=5.4, color='#555', va='center')
    ax.add_patch(plt.Rectangle((22, y), 74, 8, fc='#efefec', ec='#bbb', lw=0.5))
    for a0, a1 in seg: ax.add_patch(plt.Rectangle((a0, y), a1 - a0, 8, fc=cols[a], ec='none', alpha=0.85))
ax.annotate('', xy=(96, 8), xytext=(22, 8), arrowprops=dict(arrowstyle='-|>', color='#555', lw=0.7, mutation_scale=6))
ax.text(22, 2.5, 'start of life (high RUL)', fontsize=5.6, color='#555', ha='left', va='center'); ax.text(96, 2.5, 'failure', fontsize=5.6, color='#555', ha='right', va='center')
ax.plot([60, 60], [10, 88], color='#555', lw=0.5, ls=':'); ax.text(60, 91.5, 'RUL threshold', fontsize=5.4, color='#555', ha='center')
ax = axs[1]; rows = [r for r in S['mech']['c'] if r['h'] == 'h5'] + [r for r in S['mech']['e'] if r['h'] == 'h5']; w = 0.2
for j, (a, lab, _) in enumerate(arms):
    ax.bar(np.arange(len(rows)) + j * w - 0.3, [r['means'][a] for r in rows], w, color=cols[a], label=f'{a}: {lab}')
ax.set_xticks(range(len(rows))); ax.set_xticklabels(['FD001', 'FD002', 'FD003', 'FD004', 'DS03–DS08'], fontsize=6.5)
ax.set_title('(b) Over-estimation near end of life, last 5 cycles available', fontsize=7.5); ax.set_ylabel('mean signed error (cycles)'); ax.legend(fontsize=5.8, loc='upper left', ncol=2)
ax.yaxis.grid(True, lw=0.3, color='#ddd'); ax.set_axisbelow(True); ax.axhline(0, color='#555', lw=0.6); ax.set_ylim(0, 46)
fig.tight_layout(); save(fig, 'fig7_padding'); print('ok')
