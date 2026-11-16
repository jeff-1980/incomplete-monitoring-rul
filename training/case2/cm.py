"""C-MAPSS common code (shared with Q3)."""
import os, numpy as np, torch, torch.nn as nn
from sklearn.cluster import KMeans
from scipy.stats import wilcoxon
ROOT = os.environ.get('CMAPSS_DIR', 'data/cmapss')
OUT = os.environ.get('RESULTS_DIR', 'results')
WIN, CAP = 30, 125
SENS = [2, 3, 4, 7, 8, 9, 11, 12, 13, 14, 15, 17, 20, 21]
dev = 'cuda' if torch.cuda.is_available() else 'cpu'


def raw(fd, split):
    a = np.loadtxt(f'{ROOT}/{split}_{fd}.txt')
    return {int(u): a[a[:, 0] == u] for u in np.unique(a[:, 0])}


def test_rul(fd):
    return np.loadtxt(f'{ROOT}/RUL_{fd}.txt')


class Norm:
    def __init__(s, engines, k=6, unit_centre=False):
        A = np.concatenate(list(engines.values())); s.k = k if len(np.unique(A[:, 2:5].round(2), axis=0)) > 3 else 1
        s.km = KMeans(s.k, n_init=5, random_state=0).fit(A[:, 2:5]) if s.k > 1 else None
        r = s.regime(A); X = A[:, [4 + i for i in SENS]]
        s.mu = np.stack([X[r == j].mean(0) for j in range(s.k)]); s.sd = np.stack([X[r == j].std(0) + 1e-6 for j in range(s.k)])
        s.unit_centre = unit_centre

    def regime(s, A):
        return s.km.predict(A[:, 2:5]) if s.km is not None else np.zeros(len(A), int)

    def __call__(s, e):
        r = s.regime(e); Z = (e[:, [4 + i for i in SENS]] - s.mu[r]) / s.sd[r]
        if s.unit_centre: Z = Z - Z[:10].mean(0)
        return Z.astype(np.float32)


class GRU(nn.Module):
    def __init__(s, d, h=64):
        super().__init__(); s.rnn = nn.GRU(d, h, batch_first=True); s.head = nn.Sequential(nn.Linear(h, 32), nn.ReLU(), nn.Linear(32, 1))

    def forward(s, x):
        o, _ = s.rnn(x); return s.head(o[:, -1]).squeeze(-1)


def train(X, Y, seed, kind=None, epochs=30, bs=256):
    torch.manual_seed(seed); np.random.seed(seed)
    X = torch.tensor(X).to(dev); Y = torch.tensor(Y / CAP, dtype=torch.float32).to(dev)
    K = torch.zeros(len(Y), device=dev) if kind is None else torch.tensor(kind, dtype=torch.float32).to(dev)
    m = GRU(X.shape[-1]).to(dev); opt = torch.optim.Adam(m.parameters(), 1e-3); n = len(X)
    steps = max(30, n // bs)
    for ep in range(epochs):
        for i in range(steps):
            j = torch.randint(0, n, (bs,), device=dev); p = m(X[j]); d = p - Y[j]
            loss = torch.where(K[j] > 0, torch.relu(-d) ** 2, d ** 2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
    return m


@torch.no_grad()
def predict(m, X):
    m.eval(); return np.concatenate([m(torch.tensor(X[i:i + 8192]).to(dev)).cpu().numpy() for i in range(0, len(X), 8192)]) * CAP


def rmse(e): return float(np.sqrt(np.mean(np.square(e))))
