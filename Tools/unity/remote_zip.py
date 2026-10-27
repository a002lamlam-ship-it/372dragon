"""Seekable HTTP byte-range ZIP reader. Refuses ignored or truncated ranges."""
import io,urllib.request
from pathlib import Path
class RemoteZip(io.RawIOBase):
 def __init__(self,url,size):self.url=url;self.size=size;self.pos=0;self.transferred=0
 def seekable(self):return True
 def readable(self):return True
 def tell(self):return self.pos
 def seek(self,offset,whence=0):
  self.pos=offset if whence==0 else (self.pos+offset if whence==1 else self.size+offset)
  return self.pos
 def read(self,n=-1):
  n=self.size-self.pos if n<0 else min(n,self.size-self.pos)
  if n<=0:return b''
  end=self.pos+n-1
  req=urllib.request.Request(self.url,headers={'Range':f'bytes={self.pos}-{end}'})
  with urllib.request.urlopen(req,timeout=60) as r:
   if r.status!=206 or r.headers.get('Content-Range')!=f'bytes {self.pos}-{end}/{self.size}':raise ValueError('Server did not honor byte range')
   data=r.read(n+1)
  if len(data)!=n:raise ValueError('Incomplete range')
  self.pos+=n;self.transferred+=n
  return data
