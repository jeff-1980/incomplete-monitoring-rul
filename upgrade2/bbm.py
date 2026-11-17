"""Backbones and training for upgrade step 2 (PROTOCOL_upgrade2.md)."""
import numpy as np, torch, torch.nn as nn
torch.backends.cudnn.benchmark = True
dev = 'cuda' if torch.cuda.is_available() else 'cpu'; CAP = 125
GRID = [(32, 1e-3), (32, 3e-4), (64, 1e-3), (64, 3e-4)]


class Block(nn.Module):
    def __init__(s, c, d):
        super().__init__(); s.p = 2 * d
        s.c1 = nn.Conv1d(c, c, 3, dilation=d, padding=s.p); s.c2 = nn.Conv1d(c, c, 3, dilation=d, padding=s.p); s.a = nn.ReLU()

    def forward(s, x):
        y = s.a(s.c1(x)[..., :-s.p]); y = s.c2(y)[..., :-s.p]; return s.a(x + y)


class TCN(nn.Module):
    def __init__(s, d, c):
        super().__init__(); s.inp = nn.Conv1d(d, c, 1); s.blocks = nn.Sequential(*[Block(c, k) for k in (1, 2, 4, 8, 16)])
        s.head = nn.Sequential(nn.Linear(c, 32), nn.ReLU(), nn.Linear(32, 1))

    def forward(s, x):
        return s.head(s.blocks(s.inp(x.transpose(1, 2)))[..., -1]).squeeze(-1)


class TF(nn.Module):
    def __init__(s, d, c, maxlen=150):
        super().__init__(); s.emb = nn.Linear(d, c); s.pos = nn.Parameter(torch.zeros(maxlen, c)); nn.init.normal_(s.pos, std=0.02)
        s.enc = nn.TransformerEncoder(nn.TransformerEncoderLayer(c, 4, 2 * c, 0.1, batch_first=True), 2)
        s.head = nn.Sequential(nn.Linear(c, 32), nn.ReLU(), nn.Linear(32, 1))

    def forward(s, x):
        T = x.shape[1]; return s.head(s.enc(s.emb(x) + s.pos[-T:])[:, -1]).squeeze(-1)


def make(backbone, d, c): return TCN(d, c) if backbone == 'tcn' else TF(d, c)


def train(backbone, X, Y, seed, cfg, epochs=30, bs=256):
    c, lr = cfg; torch.manual_seed(seed); np.random.seed(seed)
    X = torch.tensor(X).to(dev); Y = torch.tensor(Y / CAP, dtype=torch.float32).to(dev)
    m = make(backbone, X.shape[-1], c).to(dev); opt = torch.optim.Adam(m.parameters(), lr); n = len(X); m.train()
    for ep in range(epochs):
        for i in range(max(30, n // bs)):
            j = torch.randint(0, n, (bs,), device=dev); loss = ((m(X[j]) - Y[j]) ** 2).mean()
            opt.zero_grad(); loss.backward(); opt.step()
    m.eval(); return m


@torch.no_grad()
def predict(m, X):
    m.eval(); return np.concatenate([m(torch.tensor(X[i:i + 4096]).to(dev)).cpu().numpy() for i in range(0, len(X), 4096)]) * CAP


def rmse(e): return float(np.sqrt(np.mean(np.square(e))))
