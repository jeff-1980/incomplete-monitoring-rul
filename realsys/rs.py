"""Battery missingness-simulation check (PROTOCOL_realsys.md). Usage: python3 rs.py <mit|xjtu> <fold> <export_dir> [smoke]
smoke: one epoch, one seed, prints shapes and timing only, writes nothing."""
import sys, json, os, time, numpy as np, rslib as R
ds, fold, exp = sys.argv[1], int(sys.argv[2]), sys.argv[3]; smoke = len(sys.argv) > 4
cap = R.CAPS[ds]; cells = R.load(ds, exp); F = R.folds(cells); os.makedirs('results', exist_ok=True)
test = sorted(k for k in cells if F[k] == fold); val = sorted(k for k in cells if F[k] == (fold + 1) % R.FOLDS)
trs = sorted(k for k in cells if F[k] not in (fold, (fold + 1) % R.FOLDS)); tr = sorted(trs + val)
print(ds, 'fold', fold, 'cells', len(cells), 'train', len(tr), 'val', len(val), 'test', len(test), flush=True)
ep = 1 if smoke else 30
# ---------- share r of complete windows: chosen on validation cells (seed 0); test cells not read ----------
nms = R.Norm(cells, trs); Xv, yv, _ = R.eval_set(cells, val, nms, cap); sc = {}
for r in (R.RS[:1] if smoke else R.RS):
    t0 = time.time(); X, Y = R.build(cells, trs, nms, 'MIX', np.random.default_rng(0), cap, r); t1 = time.time(); m = R.train(X, Y, 0, cap, ep)
    v = [R.rmse(R.predict(m, Xv[s], cap) - yv) for s in ('full', 'k10')]; sc[str(r)] = dict(full=v[0], k10=v[1], score=float(np.mean(v)))
    print('select', ds, fold, r, X.shape, 'build %.0fs train %.0fs' % (t1 - t0, time.time() - t1), '' if smoke else sc[str(r)], flush=True); del X
if smoke: sys.exit()
rstar = min(R.RS, key=lambda r: sc[str(r)]['score']); print('rstar', ds, fold, rstar, flush=True)
# ---------- final models on training + validation cells ----------
nm = R.Norm(cells, tr); Xt, yt, own = R.eval_set(cells, test, nm, cap)
err = {s: {a: [] for a in ('DENSE', 'GEN', 'MIX')} for s in Xt}
for seed in range(5):
    rng = np.random.default_rng(seed)
    for arm, r in (('DENSE', 0.0), ('GEN', 0.0), ('MIX', rstar)):
        X, Y = R.build(cells, tr, nm, arm, rng, cap, r); m = R.train(X, Y, seed, cap); del X
        for s in Xt: err[s][arm].append((R.predict(m, Xt[s], cap) - yt).tolist())
    print(ds, fold, seed, {s: {a: round(R.rmse(np.array(v[-1])), 1) for a, v in err[s].items()} for s in err}, flush=True)
json.dump(dict(sel=sc, rstar=rstar, val=val, test=test, owner=own.tolist(), y=yt.tolist(), err=err), open(f'results/rs_{ds}_f{fold}.json', 'w'))
