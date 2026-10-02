import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FD='/home/user/ugc-prod/fonts/brand/'
def F(size, italic, weight):
    f=ImageFont.truetype(FD+('PlayfairDisplay-Italic-wght.ttf' if italic else 'PlayfairDisplay-wght.ttf'), size)
    f.set_variation_by_name((weight+' Italic' if italic and weight!='Regular' else ('Italic' if italic else weight)) if italic else weight)
    return f
def caption(words, hl, size, W, weight='SemiBold'):
    """words list; hl set of indexes (blue italic). returns RGBA PIL image W wide, centred."""
    while True:
        fonts=[F(size, i in hl, weight) for i in range(len(words))]
        sp=F(size,False,weight).getlength(' ')
        ws=[f.getlength(w,features=['lnum']) for f,w in zip(fonts,words)]
        total=sum(ws)+sp*(len(words)-1)
        if total<=W-120 or size<40: break
        size=int(size*(W-120)/total)
    H=int(size*1.6); im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    x=(W-total)/2; y=int(size*0.2)
    for i,(w,f) in enumerate(zip(words,fonts)):
        d.text((x,y),w,font=f,fill=(158,197,250,255) if i in hl else (252,250,246,255),features=['lnum']); x+=ws[i]+sp
    a=np.asarray(im).astype(np.float32)
    sh=np.zeros_like(a); sh[...,0]=40; sh[...,1]=28; sh[...,2]=22
    al=cv2.GaussianBlur(a[...,3],(0,0),size*0.06)*0.85; sh[...,3]=np.clip(al*1.4,0,255)
    out=sh.copy(); A=a[...,3:4]/255; out[...,:3]=a[...,:3]*A+sh[...,:3]*(1-A); out[...,3]=np.maximum(a[...,3],sh[...,3])
    return out
