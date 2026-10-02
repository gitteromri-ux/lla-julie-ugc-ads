import sys,os,numpy as np,cv2
HB=sys.argv[1]; OUT=sys.argv[2]; sys.path.insert(0,HB)
from brandcards import *
from capstyle import caption
def card(fmt,big,sub,small):
    H=1920 if fmt=='9x16' else 1080; off=0 if fmt=='9x16' else 409
    bg=cv2.imread(HB+('/cardbg9.png' if fmt=='9x16' else '/cardbg1b.png'))
    ls=[(big,min(177,size_for(big,940)),False,WHITE,790-off)]
    if sub: ls.append((sub,min(80,size_for(sub,940,True)),True,BLUE,1030-off))
    if small: ls.append((small,min(60,size_for(small,940,True)),True,WHITE,1140-off))
    L=text_layer(1080,H,ls); R=rule_layer(1080,H,(1250 if small else (1150 if sub else 1040))-off,470,610)
    im=comp(bg,L); im=comp(im,R); return im
def put(img,L,y):
    a=L[...,3:4]/255.0; h=L.shape[0]; o=img.astype(np.float32); o[y:y+h]=o[y:y+h]*(1-a)+L[...,:3][...,::-1]*a; return o.astype(np.uint8)
for fmt in ('9x16','1x1'):
    cv2.imwrite(f'{OUT}/c28_{fmt}.png',card(fmt,'28 vs 61.','Same birth year. Same age, 38.','Dunedin Study, 954 New Zealanders.'))
    cv2.imwrite(f'{OUT}/cno2_{fmt}.png',card(fmt,'No. 2.','Slowest-aging person measured.','Rejuvenation Olympics, 2023.'))
    a=card(fmt,'As seen on','','')
    cap=caption(['In','2023,'],{1},96 if fmt=='9x16' else 80,1080)
    a=put(a,cap,1180 if fmt=='9x16' else 760)
    cv2.imwrite(f'{OUT}/cas_{fmt}.png',a)
print('cards ok')
