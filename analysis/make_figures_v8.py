"""Figures for manuscript v7: consistent arm styles across all figures; N-CMAPSS panels use twin-grouped results."""
import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

B = str(__import__('pathlib').Path(__file__).resolve().parents[1]) + ''; F = B + '/figures'
S = json.load(open(B + '/analysis/summary.json')); SQ = json.load(open(B + '/analysis/summary_q3d.json'))
S6 = json.load(open(B + '/analysis/summary_q6.json')); G = json.load(open(B + '/analysis/round3_checks.json'))
INK = '#2b2b29'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.linewidth': 0.6, 'axes.edgecolor': '#555', 'xtick.color': '#555',
                     'ytick.color': '#555', 'axes.spines.top': False, 'axes.spines.right': False, 'legend.frameon': False})
# one style per role, shared by both cases
ST = {'dense': ('#8a8a85', 'o', '--'), 'interp': ('#b5b5ae', 's', '--'), 'cf': ('#9a6324', 'x', '--'), 'zero': ('#b5b5ae', 's', '--'),
      'longdense': ('#eda100', 'v', ':'), 'imp': ('#e87ba4', '^', ':'), 'nochan': ('#b07ccf', '^', '-'), 'prop': ('#2a78d6', 'o', '-'),
      'grud': ('#008300', 'D', '-'), 'longmatched': ('#eb6834', 's', '-'), 'specific': ('#1baf7a', 'P', '-'), 'trunc': ('#b07ccf', '^', '-'), 'pcm': ('#6b3fa0', '*', '-')}
def save(fig, n): fig.savefig(f'{F}/{n}.png', dpi=300, bbox_inches='tight'); fig.savefig(f'{F}/{n}.pdf', bbox_inches='tight'); plt.close(fig)
def eb(ax, x, y, e, role, lab=None):
    c, m, ls = ST[role]; ax.errorbar(x, y, yerr=e, color=c, marker=m, ms=2.8, lw=1.25 if ls == '-' else 0.85, ls=ls, label=lab, capsize=1.2, elinewidth=0.5)
def grid(ax): ax.yaxis.grid(True, lw=0.3, color='#ddd'); ax.set_axisbelow(True)

# ---------- Fig 1 ----------
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.3))
rng = np.random.default_rng(3); T = 130; t = np.arange(T); x = 0.15 * np.exp(t / 50) + rng.normal(0, 0.05, T)
ax = axs[0]; ax.plot(t, x, color='#cfcfc9', lw=0.8); ax.scatter(t[-30:], x[-30:], s=6, color=ST['dense'][0])
ax.set_title('(a) Standard: 30 consecutive cycles', fontsize=7.5)
ax = axs[1]; ax.plot(t, x, color='#cfcfc9', lw=0.8)
idx = [T - 1]
for g in rng.integers(1, 6, 29):
    if idx[-1] - g < 0: break
    idx.append(idx[-1] - g)
idx = np.array(idx[::-1]); ax.scatter(idx, x[idx], s=8, color=ST['prop'][0])
ax.set_title('(b) Case 1: 30 records, random gaps\n(A5: gap as extra channel)', fontsize=7.5)
ax = axs[2]; ax.plot(t, x, color='#cfcfc9', lw=0.8); m = 8
ax.scatter(t[-m:], x[-m:], s=8, color=ST['prop'][0]); ax.scatter(t[-30:-m], np.full(30 - m, x[-m]), s=6, facecolors='none', edgecolors=ST['prop'][0], lw=0.6)
ax.set_title('(c) Case 2: last m cycles kept, rest filled\n(S4: filled rows flagged)', fontsize=7.5)
for ax in axs: ax.set_xlabel('cycle'); ax.set_yticks([]); ax.set_xlim(60, 132)
fig.tight_layout(); save(fig, 'fig1_method')

# ---------- Fig 2: case 1 pre-specified run ----------
arms = [('A1', 'A1 dense, raw', 'dense'), ('A2', 'A2 dense + interpolation', 'interp'), ('A3', 'A3 dense + carry-forward', 'cf'),
        ('A6', 'A6 dense, long input', 'longdense'), ('A7', 'A7 interval-specific', 'specific'), ('A4', 'A4 matched, no channel', 'nochan'),
        ('A5', 'A5 matched + gap channel', 'prop')]
sc_c = ['k1', 'k2', 'k3', 'k5', 'irr5', 'irr10']
fig, axs = plt.subplots(1, 5, figsize=(7.4, 2.7))
for ax, fd in zip(axs[:4], ['FD001', 'FD002', 'FD003', 'FD004']):
    for a, lab, role in arms:
        xs, ys, es = [], [], []
        for i, sc in enumerate(sc_c):
            k = f'{fd}|{sc}|{a}'
            if k in S['cmapss']: xs.append(i); ys.append(S['cmapss'][k]['rmse']); es.append(S['cmapss'][k]['sd'])
        eb(ax, xs, ys, es, role, lab)
    ax.set_title(fd, fontsize=8); ax.set_xticks(range(6)); ax.set_xticklabels(['1', '2', '3', '5', 'i5', 'i10'], fontsize=6.5)
    ax.set_xlabel('interval k', fontsize=6.5); ax.axvspan(4.5, 5.5, color='#f3f3f1', zorder=0); grid(ax)
ax = axs[4]
for a, lab, role in arms:
    xs, ys = [], []
    for i, sc in enumerate(['k1', 'k5', 'irr5']):
        k = f'grp|Q3 首次|{sc}|{a}'
        if k in G: xs.append(i); ys.append(G[k])
    eb(ax, xs, ys, None, role)
ax.set_title('N-CMAPSS (16 groups)', fontsize=8); ax.set_xticks(range(3)); ax.set_xticklabels(['1', '5', 'i5'], fontsize=6.5); ax.set_xlabel('interval k', fontsize=6.5); grid(ax)
axs[0].set_ylabel('RMSE (cycles)')
h, l = axs[0].get_legend_handles_labels(); fig.legend(h, l, loc='lower center', ncol=4, fontsize=6.2, bbox_to_anchor=(0.5, -0.15))
fig.tight_layout(); save(fig, 'fig2_scenarios')

# ---------- Fig 3: paired effects ----------
rows = []
for fd in ['FD001', 'FD002', 'FD003', 'FD004']: rows.append((f'{fd} k=1 vs A1 (H2)', S['H2: k1, A5 vs A1'][f'{fd}|k1']))
for r in S['H1']: rows.append((f"{r['fd']} {'k=5' if r['sc']=='k5' else 'irr'} vs {r['best']} (H1)", dict(d=r['d'], ci=r['ci'])))
for fd in ['FD001', 'FD002', 'FD003', 'FD004']: rows.append((f'{fd} k=5 vs A4', S['H3: A5 vs A4 (gap channel)'][f'{fd}|k5']))
for fd in ['FD001', 'FD002', 'FD003', 'FD004']: rows.append((f'{fd} k=5 vs A7', S['H5: A5 vs A7 (interval-matched)'][f'{fd}|k5']))
for fd in ['FD001', 'FD002', 'FD003', 'FD004']: rows.append((f'{fd} k=1 vs A6', S['H4: A5 vs A6 (long window)'][f'{fd}|k1']))
for fd in ['FD001', 'FD002', 'FD003', 'FD004']: rows.append((f'{fd} k=5 vs A6', S['H4: A5 vs A6 (long window)'][f'{fd}|k5']))
fig, ax = plt.subplots(figsize=(5.2, 6.4)); y = np.arange(len(rows))[::-1]
for yi, (lab, r) in zip(y, rows):
    c = '#2a78d6' if r['ci'][1] < 0 else ('#eb6834' if r['ci'][0] > 0 else '#8a8a85')
    ax.plot(r['ci'], [yi, yi], color=c, lw=1.2); ax.plot(r['d'], yi, 'o', color=c, ms=4)
ax.axvline(0, color='#999', lw=0.7); ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=6.5)
for gpos in (3.5, 11.5, 15.5, 19.5, 23.5): ax.axhline(len(rows) - 1 - gpos, color='#e3e3e0', lw=0.6)
ax.set_xlabel('Δ mean absolute error, A5 − reference (cycles)\n95% bootstrap interval over engines', fontsize=7)
ax.text(0.02, 1.01, '← A5 better', transform=ax.transAxes, fontsize=6.5, color='#2a78d6'); ax.text(0.98, 1.01, 'A5 worse →', transform=ax.transAxes, fontsize=6.5, color='#eb6834', ha='right')
fig.tight_layout(); save(fig, 'fig3_paired_effects')

# ---------- Fig 4: case 1 same-run batch ----------
impl = [('A1', 'A1 dense, raw', 'dense'), ('A2', 'A2 dense + interpolation', 'interp'), ('A6', 'A6 dense, long input', 'longdense'),
        ('B2s_imputer', 'IMP imputer + dense', 'imp'), ('A5', 'A5 matched + gap channel', 'prop'), ('B1_GRUD', 'GRU-D, matched', 'grud'),
        ('A8', 'A8 matched, long input', 'longmatched'), ('B4_PCMambaSDE', 'PC-MambaSDE, matched*', 'pcm')]
fig, axs = plt.subplots(1, 4, figsize=(7.4, 2.8))
for ax, fd in zip(axs, ['FD001', 'FD002', 'FD003', 'FD004']):
    for a, lab, role in impl:
        eb(ax, range(6), [SQ[f'{fd}|{sc}|{a}']['rmse'] for sc in sc_c], [SQ[f'{fd}|{sc}|{a}']['sd'] for sc in sc_c], role, lab)
    ax.set_title(fd, fontsize=8); ax.set_xticks(range(6)); ax.set_xticklabels(['1', '2', '3', '5', 'i5', 'i10'], fontsize=6.5); ax.set_xlabel('interval k', fontsize=6.5); grid(ax)
axs[0].set_ylabel('RMSE (cycles)')
h, l = axs[0].get_legend_handles_labels(); fig.legend(h, l, loc='lower center', ncol=4, fontsize=6.2, bbox_to_anchor=(0.5, -0.14))
fig.tight_layout(); save(fig, 'fig4_implementations')

# ---------- Fig 5: case 2 ----------
arm6 = [('A1', 'S1 dense, repeat pad', 'dense'), ('A2', 'S2 dense, zero pad', 'zero'), ('A6L', 'S6 dense, long input', 'longdense'),
        ('B2', 'S4 truncation + indicator', 'prop'), ('C8', 'S8 truncation, long input', 'longmatched')]
fig, axs = plt.subplots(1, 5, figsize=(7.4, 2.6))
for ax, fd in zip(axs[:4], ['FD001', 'FD002', 'FD003', 'FD004']):
    hs = ['full', 'h20', 'h10', 'h5']
    for a, lab, role in arm6:
        eb(ax, range(4), [S6[f'c|{fd}|{h}|{a}']['rmse'] for h in hs], [S6[f'c|{fd}|{h}|{a}']['sd'] for h in hs], role, lab)
    ax.set_title(fd, fontsize=8); ax.set_xticks(range(4)); ax.set_xticklabels(['all', '20', '10', '5'], fontsize=6.5); ax.set_xlabel('cycles available', fontsize=6.5); grid(ax)
ax = axs[4]
for a, lab, role in arm6:
    eb(ax, range(3), [G[f'grp|Q6|{h}|{a}'] for h in ('full', 'h5', 'h3')], None, role)
ax.set_title('N-CMAPSS (16 groups)', fontsize=8); ax.set_xticks(range(3)); ax.set_xticklabels(['all', '5', '3'], fontsize=6.5); ax.set_xlabel('cycles available', fontsize=6.5); grid(ax)
axs[0].set_ylabel('RMSE (cycles)')
h, l = axs[0].get_legend_handles_labels(); fig.legend(h, l, loc='lower center', ncol=5, fontsize=6.2, bbox_to_anchor=(0.5, -0.1))
fig.tight_layout(); save(fig, 'fig5_short_history')
print('all figures ok')
