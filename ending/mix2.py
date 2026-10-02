import sys,subprocess,numpy as np,wave,mus
SR=48000;FF='ffmpeg'
def rd(p,ss=0,d=None):
    c=[FF,'-v','error']+(['-ss',str(ss)] if ss else [])+(['-t',str(d)] if d else [])+['-i',p,'-ac','2','-ar',str(SR),'-f','f32le','-']
    return np.frombuffer(subprocess.run(c,capture_output=True).stdout,np.float32).reshape(-1,2).copy()
h=sys.argv[1]; cut=float(sys.argv[2]); drop=float(sys.argv[3]); T=float(sys.argv[4]); N=int(round(T*SR))
track=rd('hb/sonilo.m4a'); ex=rd('hb/Exhilarate.mp3',66.0,75)
ref=track[18*SR:93*SR]; k=np.sqrt((ex**2).mean())/np.sqrt((ref**2).mean()+1e-9)
music,dropad,hitad=mus.edit(track*k,drop,T=T,hit_lo=T-1.3,hit_hi=T-0.7)
if h=='ad1':
    v=rd('hb/voice24.flac',0,75); g=np.repeat(np.load('hb/g24.npy'),480)
else:
    v=np.load(f'out/{h}_voice.npy'); g=np.load(f'out/{h}_g.npy')
c=int(cut*SR); v=v[:c]; f=int(0.06*SR); v[-f:]*=np.linspace(1,0,f)[:,None]; v=np.vstack([v,np.zeros((N-len(v),2),np.float32)])[:N]
g=g.astype(np.float32)[:c]; g=np.concatenate([g,np.zeros(N-len(g),np.float32)])
ve=np.sqrt((v.mean(1)[:N//480*480].reshape(-1,480)**2).mean(1)); thr=max(1e-3,np.percentile(ve[:c//480],95)*0.03)
last=c; gmax=float(np.percentile(g[int(drop*SR):c],90))
g[last:]=gmax                                   # full energy from the cut (culmination) to the end
act=np.repeat(ve>thr,480)[:N]; act=np.concatenate([act,np.zeros(N-len(act),bool)])
gap=np.zeros(N,np.float32); mn=int(0.35*SR); pad=int(0.06*SR)
d=np.diff(np.concatenate([[1],act.astype(np.int8),[1]])); st=np.nonzero(d==-1)[0]; en=np.nonzero(d==1)[0]
for a,b in zip(st,en):
    if b-a>=mn and a<last: gap[a+pad:max(a+pad,b-pad)]=1
kk=int(0.12*SR); gap=np.convolve(gap,np.ones(kk)/kk,'same'); g=np.maximum(g,gap*gmax*0.75)
d0=int(drop*SR); r=int(0.35*SR); lift=np.full(last-d0,gmax*0.5,np.float32); lift[:r]*=np.linspace(0.3,1,r); g[d0:last]=np.maximum(g[d0:last],lift)
fe=int(0.25*SR); g[-fe:]*=np.linspace(1,0,fe)
mix=v+music*g[:,None]
with wave.open(f'out/{h}.wav','wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes())
print(h,'cut',cut,'drop',round(dropad,2),'hit',round(hitad,2),'T',T)
