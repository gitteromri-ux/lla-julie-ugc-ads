import sys,os,subprocess,json,numpy as np,cv2,wave
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from brandcards import *
from capstyle import caption
HB=os.path.dirname(os.path.abspath(__file__))+'/'
FF='ffmpeg'; FPS=24; SR=48000
HOOK=sys.argv[1]; SRCV=sys.argv[2]; OUTD=sys.argv[3]
CC={}; GRAD={}
STRAP={'9x16':caption(['The','Longevity','Masterclass','of','the','Year'],{3,4,5},54,1080,'Regular'),'1x1':caption(['The','Longevity','Masterclass','of','the','Year'],{3,4,5},50,1080,'Regular')}
BG={'9x16':cv2.imread(HB+'cardbg9.png'),'1x1':cv2.imread(HB+'cardbg1b.png')}
SUB=80
def put_layer(img,L,y):
    a=L[...,3:4]/255.0; h=L.shape[0]; o=img.astype(np.float32); o[y:y+h]=o[y:y+h]*(1-a)+L[...,:3][...,::-1]*a; return o.astype(np.uint8)
CC={}
def cap(img,words,hl,y,size):
    k=(tuple(words),tuple(sorted(hl)),size)
    if k not in CC:
        Lc=caption(words,hl,size,980); P_=np.zeros((Lc.shape[0],1080,4),np.float32); P_[:,50:1030]=Lc; CC[k]=P_
    return put_layer(img,CC[k],y)
STRAP={'9x16':caption(['The','Longevity','Masterclass','of','the','Year'],{3,4,5},54,1080,'Regular'),'1x1':caption(['The','Longevity','Masterclass','of','the','Year'],{3,4,5},50,1080,'Regular')}
GRAD={}
def topgrad(H,h):
    if (H,h) not in GRAD:
        g=np.zeros((H,1,1),np.float32); g[:h,0,0]=np.linspace(0.55,0,h)**1.2; GRAD[(H,h)]=g
    return GRAD[(H,h)]
def strap(img,fmt):
    if fmt=='9x16':
        g=topgrad(1920,0) ; y=262
        o=img.astype(np.float32); band=np.zeros_like(o); m=np.zeros((1920,1,1),np.float32); m[230:400,0,0]=np.hanning(170)*0.45
        o=o*(1-m)+np.array([34,11,0],np.float32)*m; img=o.astype(np.uint8)
        return put_layer(img,STRAP['9x16'],y)
    o=img.astype(np.float32); m=topgrad(1080,150); o=o*(1-m)+np.array([34,11,0],np.float32)*m
    return put_layer(o.astype(np.uint8),STRAP['1x1'],10)
def punch(img,s,cy=760):
    if s==1.0: return img
    H,W=img.shape[:2]; M=np.float32([[s,0,(1-s)*540],[0,s,(1-s)*cy]]); return cv2.warpAffine(img,M,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
# ---------- cards ----------
BG={'9x16':cv2.imread('/tmp/claude-0/a/r14/cardbg9.png'),'1x1':cv2.imread('/tmp/claude-0/a/r14/cardbg1b.png')}
BGN={'9x16':cv2.imread('/tmp/claude-0/a/r13/bg9.png'),'1x1':cv2.imread('/tmp/claude-0/a/r13/bg1.png')}
SUB=80
def mk(fmt,ls,ry):
    H=1920 if fmt=='9x16' else 1080
    L=text_layer(1080,H,ls); R_=rule_layer(1080,H,ry,470,610)
    A=L[...,3:4]/255; Rm=R_[...,3:4]/255; L2=L.copy(); L2[...,:3]=L[...,:3]*A*(1-Rm)+R_[...,:3]*Rm; L2[...,3]=np.maximum(L[...,3],R_[...,3]); return L2
def ease(a): a=max(0.0,min(1.0,a)); return a*a*(3-2*a)
def wide1(f,H=1170,S=34):
    W_=int(round(1080*1080/H)); r=cv2.resize(f[0:H],(W_,1080),interpolation=cv2.INTER_AREA); p=(1080-W_)//2; q=1080-W_-p
    L=cv2.resize(r[:,:S],(S+p,1080),interpolation=cv2.INTER_LINEAR); Rr=cv2.resize(r[:,W_-S:],(S+q,1080),interpolation=cv2.INTER_LINEAR)
    return np.ascontiguousarray(np.hstack([L,r[:,S:W_-S],Rr]))

H={'h2':dict(a0=0.0,caps=[(0.0,1.10,"Eight weeks",{0,1}),(1.10,2.14,"of lifestyle change",set()),(2.14,2.90,"made people's",set()),(2.90,3.62,"DNA test",{0}),(3.62,5.54,"3 years younger.",{0,1,2}),(5.54,6.68,"Food, sleep,",set()),(6.68,9.0,"exercise and stress.",{2})],
          card=('3 years younger.','In eight weeks.','Clinical trial, men 50 to 72. Aging, 2021.')),
   'h3':dict(a0=10.30,caps=[(10.64,11.46,"Five habits",{0,1}),(11.46,12.20,"at age 50",{2}),(12.20,12.84,"add up to",set()),(12.84,13.54,"14 years",{0,1}),(13.54,14.88,"to your life.",set()),(14.88,15.38,"Harvard tracked",{0}),(15.38,16.94,"123,000 people",{0}),(16.94,19.30,"for over 30 years.",{2,3})],
          card=('Up to 14 years.','Five habits. From age 50.','Harvard: 123,000 people, over 30 years.')),
   'h4':dict(a0=20.00,caps=[(20.28,21.04,"Not moving",{1}),(21.04,21.58,"your body",set()),(21.58,22.26,"is deadlier",{1}),(22.26,23.52,"than smoking.",set()),(23.52,24.24,"In a study of",set()),(24.24,26.18,"122,000 patients,",{0}),(26.18,27.24,"the least fit had",{2}),(27.24,27.98,"5 times",{0,1}),(27.98,29.0,"the risk of death.",set())],
          card=('5.04 vs 1.41.','Risk of death: low fitness vs. smoking.','Cleveland Clinic, 122,007 patients. JAMA, 2018.'))}[HOOK]
NA,NB,C1,D0=216,72,115,426
def card_layer(fmt):
    off=0 if fmt=='9x16' else 409; big,sub,small=H['card']
    return mk(fmt,[(big,min(177,size_for(big,940)),False,WHITE,790-off),(sub,min(SUB,size_for(sub,940,True)),True,BLUE,1040-off),(small,min(56,size_for(small,900,True)),True,BLUE,1140-off)],1262-off)
CL={f:card_layer(f) for f in ('9x16','1x1')}
def dec(path,w,h,ss=None):
    a=[FF,'-v','error']+(['-ss',f'{ss:.4f}'] if ss is not None else [])+['-i',path,'-f','rawvideo','-pix_fmt','bgr24','-']
    p=subprocess.Popen(a,stdout=subprocess.PIPE,bufsize=w*h*3*4)
    while True:
        b=p.stdout.read(w*h*3)
        if len(b)<w*h*3: break
        yield np.frombuffer(b,np.uint8).reshape(h,w,3)
def enc(path,w,h):
    return subprocess.Popen([FF,'-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{w}x{h}','-r','24','-i','-','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',path],stdin=subprocess.PIPE)
E={f:enc(OUTD+f'/{HOOK}_{f}.video.mp4',1080,1920 if f=='9x16' else 1080) for f in ('9x16','1x1')}
n=0
def write(f9,f1):
    global n
    E['9x16'].stdin.write(np.ascontiguousarray(f9).tobytes()); E['1x1'].stdin.write(np.ascontiguousarray(f1).tobytes()); n+=1
# A: presenter hook
g=dec(SRCV,1080,1920,ss=H['a0'])
for j in range(NA):
    base=next(g); t=H['a0']+j/FPS
    f9=base.copy(); f1=wide1(base)
    for a,b,txt,hl in H['caps']:
        if a<=t<b:
            w=txt.split(); f9=cap(f9,w,hl,y=980,size=101); f1=cap(f1,w,hl,y=820,size=84)
    write(strap(f9,'9x16'),strap(f1,'1x1'))
g.close()
# B: stat card (hard cut to empty card, text eases in, eases out at end)
for t in range(NB):
    a=ease(t/6.0)
    if NB-t<=3: a=min(a,ease((NB-t)/3.0))
    write(comp(BG['9x16'],CL['9x16'],a),comp(BG['1x1'],CL['1x1'],a))
# C + D from approved body
G9=dec(HB+'v24_9x16.video.mp4',1080,1920); G1=dec(HB+'v24_1x1.video.mp4',1080,1080)
last=None
for k,(f9,f1) in enumerate(zip(G9,G1)):
    if k<C1 or k>=D0: write(f9,f1); last=(f9,f1)
while n<1800: write(*last)
for e in E.values(): e.stdin.close(); e.wait()
# audio
def rd(path,ss,dur):
    r=subprocess.run([FF,'-v','error','-ss',f'{ss:.4f}','-t',f'{dur:.4f}','-i',path,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    x=np.frombuffer(r,np.float32).reshape(-1,2).copy(); N=int(round(dur*SR))
    return np.vstack([x,np.zeros((max(0,N-len(x)),2),np.float32)])[:N]
def act(a):
    m=a.mean(1); m=m[:len(m)//480*480]; e=np.sqrt((m.reshape(-1,480)**2).mean(1)); thr=np.percentile(e,60); return np.sqrt((e[e>=thr]**2).mean())
fr=lambda k:int(round(k*SR/FPS))
v24=rd(HB+'voice24.flac',0,75.0)
hook=rd(SRCV,H['a0'],NA/FPS); hook*=act(v24[:fr(C1)])/act(hook)
f8=int(0.008*SR)
def fade(x,a=f8):
    x[:a]*=np.linspace(0,1,a)[:,None]; x[-a:]*=np.linspace(1,0,a)[:,None]; return x
hook=fade(hook,int(0.06*SR))
voice=np.vstack([hook,np.zeros((fr(NB),2),np.float32),fade(v24[:fr(C1)].copy()),fade(v24[fr(D0):fr(1800)].copy())])
T=75.0; N=int(T*SR); voice=np.vstack([voice,np.zeros((N-len(voice),2),np.float32)])[:N]
g24=np.load(HB+'g24.npy'); g24=np.repeat(g24,480)[:N]
gA=np.full(fr(NA),0.0665,np.float32); gA[:int(0.12*SR)]*=np.linspace(0,1,int(0.12*SR))
gB=np.full(fr(NB),0.24,np.float32); r=int(0.25*SR); gB[:r]=np.linspace(0.0665,0.24,r); gB[-r:]=np.linspace(0.24,0.0665,r)
gD=g24[fr(D0):]
gg=np.concatenate([gA,gB,g24[:fr(C1)],gD]); gg=np.concatenate([gg,np.full(max(0,N-len(gg)),gD[-int(0.5*SR)],np.float32)])[:N]
gg=np.convolve(gg,np.ones(4800)/4800,mode='same').astype(np.float32); gg[-int(0.3*SR):]*=np.linspace(1,0,int(0.3*SR))
music=rd(HB+'Exhilarate.mp3',66.0,T)
mix=voice+music*gg[:,None]
with wave.open(OUTD+f'/{HOOK}.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes())
print('done',HOOK,n)
