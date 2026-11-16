import zipfile, requests, os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rz import RF, U
from stream_unzip import stream_unzip
OUT=os.environ.get('NCMAPSS_DIR', 'data/ncmapss'); os.makedirs(OUT,exist_ok=True)
outer=zipfile.ZipFile(RF(U,0,int(requests.head(U).headers['Content-Length'])))
inf=[i for i in outer.infolist() if i.filename.endswith('data_set.zip')][0]
src=outer.open(inf)
def chunks():
    while True:
        b=src.read(16<<20)
        if not b: return
        yield b
for name,size,it in stream_unzip(chunks()):
    name=name.decode(); base=os.path.basename(name)
    print('entry',name,size,flush=True)
    if base.endswith('.h5') or base.endswith('.pdf') or base.endswith('.txt'):
        with open(os.path.join(OUT,base),'wb') as f:
            for b in it: f.write(b)
        print('saved',base,os.path.getsize(os.path.join(OUT,base)),shutil.disk_usage('/').free//2**30,'GB free',flush=True)
    else:
        for _ in it: pass
print('ALL DONE',flush=True)
