import sys,subprocess,numpy as np,wave,mus
SR=48000;FF='ffmpeg'
def rd(p,ss=0,d=None):
    c=[FF,'-v','error']+(['-ss',str(ss)] if ss else [])+(['-t',str(d)] if d else [])+['-i',p,'-ac','2','-ar',str(SR),'-f','f32le','-']
    return np.frombuffer(subprocess.run(c,capture_output=True).stdout,np.float32).reshape(-1,2).copy()
h=sys.argv[1]; cut=float(sys.argv[2]); drop=float(sys.argv[3]); T=float(sys.argv[4]); N=int(T*SR)
track=rd('hb/sonilo.m4a'); ex=rd('hb/Exhilarate.mp3',66.0,75)
ref=track[18*SR:93*SR]; k=np.sqrt((ex**2).mean())/np.sqrt((ref**2).mean()+1e-9)
music,dropad,hitad=mus.edit(track*k,drop,T=T,hit_lo=T-1.3,hit_hi=T-0.7); music=np.vstack([music,np.zeros((max(0,N-len(music)),2),np.float32)])[:N]
if h=='ad1': v=rd('hb/voice24.flac',0,75); g0=np.repeat(np.load('hb/g24.npy'),480).astype(np.float32)
else: v=np.load(f'out/{h}_voice.npy'); g0=np.load(f'out/{h}_g.npy').astype(np.float32)
c=int(cut*SR); v=v[:c].copy(); f=int(0.06*SR); v[-f:]*=np.linspace(1,0,f)[:,None]; v=np.vstack([v,np.zeros((N-len(v),2),np.float32)])[:N]
gfull=float(max(np.percentile(g0[c:c+8*SR],90) if len(g0)>c+SR else 0.0, np.percentile(g0[:c],99)))
g=np.concatenate([g0[:c],np.full(N-c,gfull,np.float32)])[:N]
ve=np.sqrt((v.mean(1)[:N//480*480].reshape(-1,480)**2).mean(1)); thr=max(1e-3,np.percentile(ve[:c//480],95)*0.03)
act=np.repeat(ve>thr,480); act=np.concatenate([act,np.zeros(N-len(act),bool)])[:N]
gap=np.zeros(N,np.float32); mn=int(0.35*SR); pad=int(0.06*SR)
d=np.diff(np.concatenate([[1],act.astype(np.int8),[1]])); st=np.nonzero(d==-1)[0]; en=np.nonzero(d==1)[0]
for a,b in zip(st,en):
    if b-a>=mn and a<c: gap[a+pad:max(a+pad,b-pad)]=1
kk=int(0.12*SR); gap=np.convolve(gap,np.ones(kk)/kk,'same'); g=np.maximum(g,gap*gfull*0.6)
d0=int(drop*SR); r=int(0.35*SR); lift=np.full(c-d0,gfull*0.45,np.float32); lift[:r]*=np.linspace(0.3,1,r); g[d0:c]=np.maximum(g[d0:c],lift)
sm=int(0.02*SR); g[c-sm:c+sm]=np.linspace(g[c-sm],gfull,2*sm)
fe=int(0.25*SR); g[-fe:]*=np.linspace(1,0,fe)
mix=v+music*g[:,None]
with wave.open(f'out/{h}.wav','wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes())
print(h,'cut',cut,'drop',round(dropad,2),'hit',round(hitad,2),'T',T,'gfull',round(gfull,3))
