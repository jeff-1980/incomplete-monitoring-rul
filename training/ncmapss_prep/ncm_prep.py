import os, h5py, numpy as np
out={}
for ds in ['DS01-005','DS02-006']:
    f=h5py.File(os.path.join(os.environ.get('NCMAPSS_DIR', 'data/ncmapss'), f'N-CMAPSS_{ds}.h5'),'r')
    for part in ['dev','test']:
        A=np.array(f[f'A_{part}']); X=np.array(f[f'X_s_{part}']); Wc=np.array(f[f'W_{part}']); Y=np.array(f[f'Y_{part}'])[:,0]
        for u in np.unique(A[:,0]):
            m=A[:,0]==u; cyc=A[m,1]; cs=np.unique(cyc)
            feats=[];ys=[]
            for c in cs:
                mm=cyc==c; xs=X[m][mm]; ws=Wc[m][mm]
                feats.append(np.concatenate([xs.mean(0),xs.std(0),ws.mean(0)])); ys.append(Y[m][mm][0])
            key=f'{ds[:4]}_u{int(u)}_{part}'; out[key+'_X']=np.array(feats,np.float32); out[key+'_y']=np.array(ys,np.float32)
            print(key,len(cs),ys[0],ys[-1],flush=True)
np.savez('ncm_cycles.npz',**out)
