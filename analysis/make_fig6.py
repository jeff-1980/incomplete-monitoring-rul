"""Figure 6: external cohort and padding-shortcut experiment (from upgrade1/summary_upgrade1.json)."""
import json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
B = str(__import__('pathlib').Path(__file__).resolve().parents[1]) + ''; S = json.load(open(B + '/upgrade1/summary_upgrade1.json'))
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.linewidth': 0.6, 'axes.edgecolor': '#555', 'xtick.color': '#555',
                     'ytick.color': '#555', 'axes.spines.top': False, 'axes.spines.right': False, 'legend.frameon': False})
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.6), gridspec_kw={'width_ratios': [1.15, 1, 1.25]})
def bars(ax, scs, labs, arms, cols, names):
    w = 0.8 / len(arms)
    for j, (a, c, n) in enumerate(zip(arms, cols, names)):
        ax.bar(np.arange(len(scs)) + j * w - 0.4 + w / 2, [S[f'ext|{sc}|{a}'] for sc in scs], w, color=c, label=n)
    ax.set_xticks(range(len(scs))); ax.set_xticklabels(labs, fontsize=6.5); ax.yaxis.grid(True, lw=0.3, color='#ddd'); ax.set_axisbelow(True)
bars(axs[0], ['k1', 'k5', 'irr5', 'blk5', 'blk10'], ['k = 1', 'k = 5', 'irr 1–5', 'block 5', 'block 10'], ['A1', 'A2', 'A5', 'A8'],
     ['#8a8a85', '#b5b5ae', '#2a78d6', '#eb6834'], ['A1 dense, raw', 'A2 dense + interp.', 'A5', 'A8'])
axs[0].set_title('(a) External cohort, case 1', fontsize=7.5); axs[0].set_ylabel('RMSE (cycles)'); axs[0].legend(fontsize=5.8, ncol=2, loc='upper left'); axs[0].set_ylim(0, 27)
bars(axs[1], ['full', 'h5', 'h3'], ['complete', 'last 5', 'last 3'], ['S1', 'S2', 'S4', 'S8'], ['#8a8a85', '#b5b5ae', '#2a78d6', '#eb6834'],
     ['S1 repeat pad', 'S2 zero pad', 'S4', 'S8'])
axs[1].set_title('(b) External cohort, case 2', fontsize=7.5); axs[1].legend(fontsize=5.8, ncol=2, loc='upper left'); axs[1].set_ylim(0, 27)
rows = [r for r in S['mech']['c'] if r['h'] == 'h5'] + [r for r in S['mech']['e'] if r['h'] == 'h5']
arms = ['S1', 'S3E', 'S3', 'S3L']; cols = ['#8a8a85', '#9a6324', '#b07ccf', '#1baf7a']
names = ['S1 no truncation', 'S3E truncated if RUL high', 'S3 all truncated', 'S3L truncated if RUL low']; w = 0.2
for j, (a, c, n) in enumerate(zip(arms, cols, names)):
    axs[2].bar(np.arange(len(rows)) + j * w - 0.3, [r['means'][a] for r in rows], w, color=c, label=n)
axs[2].set_xticks(range(len(rows))); axs[2].set_xticklabels(['FD001', 'FD002', 'FD003', 'FD004', 'DS03–08'], fontsize=6.5)
axs[2].set_title('(c) Signed error near end of life, last 5 cycles', fontsize=7.5); axs[2].set_ylabel('mean signed error (cycles)'); axs[2].legend(fontsize=5.6, loc='upper left')
axs[2].yaxis.grid(True, lw=0.3, color='#ddd'); axs[2].set_axisbelow(True); axs[2].axhline(0, color='#555', lw=0.6); axs[2].set_ylim(0, 48)
fig.tight_layout(); fig.savefig(B + '/figures/fig6_external_mechanism.png', dpi=300, bbox_inches='tight'); fig.savefig(B + '/figures/fig6_external_mechanism.pdf', bbox_inches='tight'); print('ok')
