import subprocess,numpy as np,wave
SR=48000;FF='ffmpeg'
def rd(p,ss,d):
    r=subprocess.run([FF,'-v','error','-ss',str(ss),'-t',str(d),'-i',p,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    x=np.frombuffer(r,np.float32).reshape(-1,2).copy(); N=int(d*SR); return np.vstack([x,np.zeros((max(0,N-len(x)),2),np.float32)])[:N]
T=75.0;N=int(T*SR)
v=rd('hb/voice24.flac',0,T); ex=rd('hb/Exhilarate.mp3',66.0,T); m=rd('hb/sonilo.m4a',18.0,T); m*=np.sqrt((ex**2).mean())/np.sqrt((m**2).mean()+1e-9)
g=np.repeat(np.load('hb/g24.npy'),480)[:N]; g=np.concatenate([g,np.full(N-len(g),g[-1],np.float32)]); g[-int(0.3*SR):]*=np.linspace(1,0,int(0.3*SR))
mix=v+m*g[:,None]
with wave.open('out/ad1.wav','wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes())
print('ad1 mixed')
