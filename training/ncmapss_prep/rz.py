import zipfile, requests, io, sys, os
U="https://phm-datasets.s3.amazonaws.com/NASA/17.+Turbofan+Engine+Degradation+Simulation+Data+Set+2.zip"
class RF(io.RawIOBase):
    def __init__(s,u,base,size): s.u,s.base,s.size,s.pos=u,base,size,0; s.ses=requests.Session()
    def seekable(s): return True
    def readable(s): return True
    def tell(s): return s.pos
    def seek(s,o,w=0):
        s.pos = o if w==0 else s.pos+o if w==1 else s.size+o; return s.pos
    def read(s,n=-1):
        if n<0: n=s.size-s.pos
        if n==0 or s.pos>=s.size: return b''
        e=min(s.pos+n,s.size)-1
        r=s.ses.get(s.u,headers={'Range':f'bytes={s.base+s.pos}-{s.base+e}'},timeout=600); d=r.content; s.pos+=len(d); return d
