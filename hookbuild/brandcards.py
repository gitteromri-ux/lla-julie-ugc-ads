import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
FD='/home/user/ugc-prod/fonts/brand/'
WHITE=(250,248,245); BLUE=(158,190,235); RULE=(69,81,113)
def font(size, italic=False):
    f=ImageFont.truetype(FD+('PlayfairDisplay-Italic-wght.ttf' if italic else 'PlayfairDisplay-wght.ttf'), size)
    try: f.set_variation_by_name('Regular' if not italic else 'Italic')
    except Exception: pass
    return f
def size_for(text, width, italic=False):
    lo,hi=10,400
    while hi-lo>1:
        m=(lo+hi)//2; b=font(m,italic).getbbox(text)
        if b[2]-b[0]>width: hi=m
        else: lo=m
    return lo
def text_layer(W,H,lines):
    """lines: list of (text, size, italic, color, top_y). Returns RGBA float array."""
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    for t,s,it,c,y in lines:
        f=font(s,it); b=f.getbbox(t); w=b[2]-b[0]
        d.text(((W-w)//2-b[0], y-b[1]), t, font=f, fill=c+(255,))
    return np.asarray(im).astype(np.float32)
def rule_layer(W,H,y,x0,x1):
    a=np.zeros((H,W,4),np.float32); a[y:y+3,x0:x1,:3]=RULE[::-1] if False else RULE; a[y:y+3,x0:x1,3]=255; return a
def comp(bg_bgr, layer_rgba, alpha=1.0):
    a=layer_rgba[...,3:4]/255.0*alpha; rgb=layer_rgba[...,:3][...,::-1]
    return np.clip(bg_bgr.astype(np.float32)*(1-a)+rgb*a,0,255).astype(np.uint8)
