"""Verified HTTP range cache in a sparse file; supports bounded parallel prefetch."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from remote_zip import RemoteZip

class CachedRemoteZip(RemoteZip):
    def __init__(self,url,size,cache):
        super().__init__(url,size)
        self.cache=Path(cache)
        self.cache.parent.mkdir(parents=True,exist_ok=True)
        self.intervals=[]
        with self.cache.open('wb') as stream:stream.truncate(size)
    def record(self,start,end):
        ranges=sorted(self.intervals+[(start,end)])
        merged=[]
        for a,b in ranges:
            if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
            else:merged.append((a,b))
        self.intervals=merged
    def read(self,n=-1):
        n=self.size-self.pos if n<0 else min(n,self.size-self.pos)
        if n<=0:return b''
        start=self.pos;end=start+n
        if any(a<=start and end<=b for a,b in self.intervals):
            with self.cache.open('rb') as stream:stream.seek(start);data=stream.read(n)
            self.pos=end
            return data
        data=super().read(n)
        with self.cache.open('r+b') as stream:stream.seek(start);stream.write(data)
        self.record(start,end)
        return data
    def prefetch(self,ranges,workers=4):
        def fetch(bounds):
            start,end=bounds
            reader=RemoteZip(self.url,self.size);reader.seek(start)
            data=reader.read(end-start)
            with self.cache.open('r+b') as stream:stream.seek(start);stream.write(data)
            return start,end,len(data)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            jobs=[pool.submit(fetch,bounds) for bounds in ranges]
            for count,job in enumerate(as_completed(jobs),1):
                start,end,size=job.result();self.transferred+=size;self.record(start,end)
                if count%20==0 or count==len(jobs):print(f'Ranges {count}/{len(jobs)}; fetched {self.transferred/1048576:.1f} MiB',flush=True)
