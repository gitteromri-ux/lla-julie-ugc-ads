import re
p='/home/user/hb/hookbuild.py'; s=open(p).read()
s=s.replace("caption(['The','Longevity','Masterclass','of','the','Year'],{3,4,5},54,1080,'Regular')","caption('Learn to age slower from the 2nd slowest-aging human on Earth.'.split(),{6,7,8,9,10},54,1080,'Regular')")
s=s.replace("caption(['The','Longevity','Masterclass','of','the','Year'],{3,4,5},50,1080,'Regular')","caption('Learn to age slower from the 2nd slowest-aging human on Earth.'.split(),{6,7,8,9,10},50,1080,'Regular')")
s=re.sub(r"'h3':dict\(a0=10\.55,na=190,caps=\[.*?\]\)", "'h3':dict(a0=10.55,na=190,caps=[(10.55,18.6,'Five habits at 50 add up to 14 years.',{7,8})])", s, flags=re.S)
s=s.replace('def strap(img,fmt):','def strap(img,fmt):\n    return img\ndef _old_strap(img,fmt):',1)
open(p,'w').write(s); print('patched', s.count('2nd slowest-aging'), "'h3':dict(a0=10.55,na=190,caps=[(10.55" in s)
