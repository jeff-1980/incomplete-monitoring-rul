"""Stream the N-CMAPSS zip once; for each DS03-DS08 h5: save, aggregate to cycle-level features exactly as ncm_prep.py
(per cycle: mean and std of X_s, mean of W), record flight class Fc per unit, then delete the h5."""
import zipfile, requests, os, sys, shutil, json, numpy as np, h5py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rz import RF, U
from stream_unzip import stream_unzip
TMP = os.environ.get('NCMAPSS_DIR', 'data/ncmapss'); os.makedirs(TMP, exist_ok=True); OUT = '.'
out, fc = {}, {}
def prep(path, ds):
    f = h5py.File(path, 'r')
    for part in ['dev', 'test']:
        A = np.array(f[f'A_{part}']); X = np.array(f[f'X_s_{part}']); Wc = np.array(f[f'W_{part}']); Y = np.array(f[f'Y_{part}'])[:, 0]
        av = [a.decode() if isinstance(a, bytes) else a for a in np.array(f['A_var'])]; ifc = av.index('Fc')
        for u in np.unique(A[:, 0]):
            m = A[:, 0] == u; cyc = A[m, 1]; cs = np.unique(cyc); feats = []; ys = []
            for c in cs:
                mm = cyc == c; xs = X[m][mm]; ws = Wc[m][mm]
                feats.append(np.concatenate([xs.mean(0), xs.std(0), ws.mean(0)])); ys.append(Y[m][mm][0])
            key = f'{ds}_u{int(u)}_{part}'; out[key + '_X'] = np.array(feats, np.float32); out[key + '_y'] = np.array(ys, np.float32)
            fc[key] = int(np.round(A[m, ifc][0]))
            print(key, len(cs), ys[0], ys[-1], 'Fc', fc[key], flush=True)
    f.close()
outer = zipfile.ZipFile(RF(U, 0, int(requests.head(U).headers['Content-Length'])))
inf = [i for i in outer.infolist() if i.filename.endswith('data_set.zip')][0]; src = outer.open(inf)
def chunks():
    while True:
        b = src.read(16 << 20)
        if not b: return
        yield b
for name, size, it in stream_unzip(chunks()):
    base = os.path.basename(name.decode()); print('entry', base, size, flush=True)
    if base.endswith('.h5') and not base.startswith(('N-CMAPSS_DS01', 'N-CMAPSS_DS02')):
        p = os.path.join(TMP, base)
        with open(p, 'wb') as fh:
            for b in it: fh.write(b)
        ds = base.replace('N-CMAPSS_', '').split('-')[0]
        print('saved', base, os.path.getsize(p), shutil.disk_usage('/').free // 2**30, 'GB free', flush=True)
        prep(p, ds); os.remove(p)
        np.savez(f'{OUT}/ncm_cycles_ds03_08.npz', **out); json.dump(fc, open(f'{OUT}/ncm_fc_ds03_08.json', 'w'), indent=0)
    else:
        for _ in it: pass
print('ALL DONE', flush=True)
