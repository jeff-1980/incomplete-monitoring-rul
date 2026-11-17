"""Common code of the battery missingness-simulation check (PROTOCOL_realsys.md). Everything here is fixed by the protocol."""
import numpy as np, pandas as pd, torch, torch.nn as nn
L, KMAX, K, BLK, T0, FOLDS, SPLIT_SEED = 200, 10, 10, 50, 30, 5, 20261117
RS = (0.25, 0.5, 0.75)
CAPS = {'mit': 450.0, 'xjtu': 250.0}
FEATS = {'mit': ['discharge_capacity_Ah', 'charge_capacity_Ah', 'internal_resistance_ohm', 'temp_mean_C', 'temp_max_C', 'temp_min_C', 'charge_time_min', 'charge_energy_Wh',
                 'discharge_energy_Wh', 'charge_median_voltage', 'discharge_median_voltage', 'charge_mean_voltage', 'discharge_mean_voltage'],
         'xjtu': ['discharge_capacity_Ah', 'charge_capacity_Ah', 'temp_mean_C', 'temp_max_C', 'charge_power_Wh', 'discharge_power_Wh', 'charge_median_voltage',
                  'discharge_median_voltage', 'charge_mean_voltage', 'discharge_mean_voltage']}
dev = 'cuda' if torch.cuda.is_available() else 'cpu'


def load(ds, export_dir):
    """-> {cell: dict(batch, X [T,F] float32, typ [T] int)}; the last row of X is the end of life."""
    df = pd.read_csv(f'{export_dir}/{ds}.csv.gz', low_memory=False); out = {}
    if ds == 'xjtu':
        df = df[df.batch.isin(['Batch-1', 'Batch-2', 'Batch-3', 'Batch-4']) & (df.cycle > 1)].copy()
        df['tkey'] = df.batch + '|' + df.cycle_description
    else: df['tkey'] = 'all'
    codes = {k: i for i, k in enumerate(sorted(df.tkey.unique()))}
    for (b, c), g in df.groupby(['batch', 'battery_id']):
        g = g.sort_values('cycle'); X = g[FEATS[ds]].to_numpy(float); typ = g.tkey.map(codes).to_numpy(int)
        if ds == 'mit':
            q = X[:, 0]; eol = next((i for i in range(10, len(q) - 2) if (q[i:i + 3] < 0.88).all()), None)
            if eol is None:
                if q[-1] > 0.885: continue                       # never reached 80% of nominal capacity: excluded
                eol = len(q) - 1
            X = X[:eol + 1]; typ = typ[:eol + 1]; bad = X <= 0
            bad[:, 0] |= (X[:, 0] < 0.55) | (X[:, 0] > 1.43); bad[:, 1] |= (X[:, 1] < 0.55) | (X[:, 1] > 1.43); bad[:, 6] |= X[:, 6] > 60
            X = pd.DataFrame(np.where(bad, np.nan, X)).ffill().bfill().to_numpy(float)   # source artefacts: previous valid value
        out[f'{b}|{c}'] = dict(batch=b, X=X.astype(np.float32), typ=typ)
    return out


def folds(cells):
    """cell -> fold, stratified by batch, fixed seed."""
    rng = np.random.default_rng(SPLIT_SEED); f = {}
    for b in sorted(set(v['batch'] for v in cells.values())):
        ids = sorted(k for k, v in cells.items() if v['batch'] == b); rng.shuffle(ids)
        for i, k in enumerate(ids): f[k] = i % FOLDS
    return f


class Norm:
    def __init__(s, cells, names):
        X = np.concatenate([cells[n]['X'] for n in names]); t = np.concatenate([cells[n]['typ'] for n in names])
        s.g = (X.mean(0), X.std(0) + 1e-6); s.st = {int(k): (X[t == k].mean(0), X[t == k].std(0) + 1e-6) for k in np.unique(t)}

    def __call__(s, c):
        mu = np.stack([s.st.get(int(k), s.g)[0] for k in c['typ']]); sd = np.stack([s.st.get(int(k), s.g)[1] for k in c['typ']])
        return np.clip((c['X'] - mu) / sd, -10, 10).astype(np.float32)


def grid(Z, idx, t):
    """every-cycle window of length L ending at cycle t, linearly interpolated from the records idx (idx[-1] == t); left-padded with the first value."""
    g = np.arange(max(int(idx[0]), t - L + 1), t + 1)
    G = np.stack([np.interp(g, idx, Z[idx, j]) for j in range(Z.shape[1])], 1).astype(np.float32)
    return G if len(G) == L else np.concatenate([np.repeat(G[:1], L - len(G), 0), G])


def gen_idx(t, rng):
    """generic random deletion: every earlier cycle of the window kept independently with probability p; the last cycle is kept."""
    p = 1.0 / rng.integers(1, KMAX + 1) if rng.random() < 0.5 else 2.0 / (KMAX + 1); lo = max(0, t - L + 1)
    return np.r_[np.arange(lo, t)[rng.random(t - lo) < p], t].astype(int)


def build(cells, names, nm, kind, rng, cap, r=0.0):
    Xs, Ys = [], []
    for n in names:
        Z = nm(cells[n]); T = len(Z)
        for t in range(T):
            full = kind == 'DENSE' or (kind == 'MIX' and rng.random() < r)
            idx = np.arange(max(0, t - L + 1), t + 1) if full else gen_idx(t, rng)
            Xs.append(grid(Z, idx, t)); Ys.append(min(T - 1 - t, cap))
    return np.stack(Xs), np.array(Ys, np.float32)


def scen_idx(sc, t):
    if sc == 'full': return np.arange(0, t + 1)
    if sc == 'k10': return np.arange(0, t + 1, K)                       # t is a multiple of K
    return np.r_[np.arange(0, max(t - 2 - BLK, 0)), np.arange(t - 2, t + 1)].astype(int)   # 'blk': outage of BLK cycles before the last three


def eval_set(cells, names, nm, cap):
    """-> {scenario: X}, y, owner (cell name per row); prediction times t = T0, T0+K, ..."""
    X = {sc: [] for sc in ('full', 'k10', 'blk')}; y = []; own = []
    for n in names:
        Z = nm(cells[n]); T = len(Z)
        for t in range(T0, T, K):
            for sc in X: X[sc].append(grid(Z, scen_idx(sc, t), t))
            y.append(min(T - 1 - t, cap)); own.append(n)
    return {sc: np.stack(v) for sc, v in X.items()}, np.array(y, np.float32), np.array(own)


class GRU(nn.Module):
    def __init__(s, d, h=64):
        super().__init__(); s.rnn = nn.GRU(d, h, batch_first=True); s.head = nn.Sequential(nn.Linear(h, 32), nn.ReLU(), nn.Linear(32, 1))

    def forward(s, x):
        o, _ = s.rnn(x); return s.head(o[:, -1]).squeeze(-1)


def train(X, Y, seed, cap, epochs=30, bs=256):
    torch.manual_seed(seed); np.random.seed(seed)
    X = torch.tensor(X).to(dev); Y = torch.tensor(Y / cap, dtype=torch.float32).to(dev)
    m = GRU(X.shape[-1]).to(dev); opt = torch.optim.Adam(m.parameters(), 1e-3); n = len(X); steps = max(30, n // bs)
    for ep in range(epochs):
        for i in range(steps):
            j = torch.randint(0, n, (bs,), device=dev); loss = ((m(X[j]) - Y[j]) ** 2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
    return m


@torch.no_grad()
def predict(m, X, cap):
    m.eval(); return np.concatenate([m(torch.tensor(X[i:i + 4096]).to(dev)).cpu().numpy() for i in range(0, len(X), 4096)]) * cap


rmse = lambda e: float(np.sqrt(np.mean(np.square(e))))
