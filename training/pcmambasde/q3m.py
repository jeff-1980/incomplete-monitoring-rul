"""PC-MambaSDE (authors' released model code; only a duplicate Encoder class name was renamed so that the Mamba encoder is used, see README) under the Q3 sparse protocol.
Trained on the same mixed-interval 30-record windows as A5 (deployment sampling law); obs_times = elapsed cycles / 150
(real gaps preserved), mask = 1 (all sensors observed at a record). Loss = MSE(normalised RUL) + model aux loss
(bridge + monotonic + KL), as in the authors' train.py. Adam 1e-3, weight decay 1e-4 (authors' default), batch 256,
same number of steps as the other arms (30 epochs x n/256). Fixed epochs, no checkpoint selection on test data.
Usage: python3 q3m.py FD001 seed"""
import sys, os, json, types, numpy as np, torch, cm
PCM = os.environ.get('PCMAMBA_DIR', 'PC-MambaSDE'); sys.path.insert(0, PCM); sys.path.insert(0, os.path.join(PCM, 'sde_lib'))
from model import SDE_RUL_Adapter
from q3lib import obs_idx, win_from_obs, mixed_gaps, test_gaps, W, KMAX
fd, seed = sys.argv[1], int(sys.argv[2]); rng = np.random.default_rng(seed); dev = cm.dev
EP = int(os.environ.get('EP', 30)); SC = ('k1', 'k2', 'k3', 'k5', 'irr5', 'irr10')

def build(engines, nm):
    Xs, Ys = [], []
    for e in engines.values():
        Z = nm(e); T = len(Z)
        for t in range(T):
            Xs.append(win_from_obs(Z, obs_idx(t + 1, mixed_gaps(rng)), W, True)); Ys.append(min(T - 1 - t, cm.CAP))
    return np.stack(Xs).astype(np.float32), np.array(Ys, np.float32)

def split(xb):            # values, normalised elapsed time from the gap channel
    v = xb[..., :-1]; t = torch.cumsum(xb[..., -1] * KMAX, 1) / (W * KMAX); return v, t

def make():
    o = types.SimpleNamespace(dim_en=64, num_features=len(cm.SENS), num_enc_layers=1, drop_out=0.1, train_seq_len=W)
    m = SDE_RUL_Adapter(o).to(dev)
    for p in m.parameters():
        if p.dim() > 1:
            try: torch.nn.init.xavier_uniform_(p)
            except Exception: pass
    return m

def train(X, Y):
    torch.manual_seed(seed); m = make(); X = torch.tensor(X).to(dev); Y = torch.tensor(Y / cm.CAP).to(dev)
    opt = torch.optim.Adam(m.parameters(), 1e-3, weight_decay=1e-4); n = len(X); bs = 256
    for ep in range(EP):
        m.train(); tot = 0
        for i in range(max(30, n // bs)):
            j = torch.randint(0, n, (bs,), device=dev); v, t = split(X[j])
            p = m(v, obs_times=t, y_target=Y[j]).view(-1); loss = ((p - Y[j]) ** 2).mean() + m.aux_loss
            opt.zero_grad(); loss.backward(); opt.step(); tot += loss.item()
        print(fd, seed, 'ep', ep, f'{tot / max(30, n // bs):.4f}', flush=True)
    return m

@torch.no_grad()
def predict(m, X):
    m.eval(); out = []
    for i in range(0, len(X), 1024):
        v, t = split(torch.tensor(X[i:i + 1024]).to(dev)); out.append(m(v, obs_times=t).view(-1).cpu().numpy())
    return np.concatenate(out) * cm.CAP

tr = cm.raw(fd, 'train'); nm = cm.Norm(tr); te = cm.raw(fd, 'test'); units = sorted(te); yt = np.minimum(cm.test_rul(fd), cm.CAP)
X, Y = build(tr, nm); m = train(X, Y); Zs = [nm(te[u]) for u in units]; out = {}
for sc in SC:
    Xa = np.stack([win_from_obs(Z, obs_idx(len(Z), test_gaps(sc, u)), W, True) for Z, u in zip(Zs, units)])
    out[sc] = {'B4_PCMambaSDE': (predict(m, Xa) - yt).tolist()}
    print(fd, seed, sc, f"{cm.rmse(np.array(out[sc]['B4_PCMambaSDE'])):.2f}", flush=True)
json.dump(out, open(f'results/q3m_{fd}_s{seed}.json', 'w'))
