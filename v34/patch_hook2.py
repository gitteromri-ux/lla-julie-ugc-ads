p='/home/user/hb/hookbuild.py'; s=open(p).read()
old="""caps=[(10.64,11.46,"Five habits",{0,1}),(11.46,12.20,"at age 50",{2}),(12.20,12.84,"add up to",set()),(12.84,13.54,"14 years",{0,1}),(13.54,14.88,"to your life.",set()),(14.88,15.38,"Harvard tracked",{0}),(15.38,16.94,"123,000 people",{0}),(16.94,19.30,"for over 30 years.",{2,3})]"""
assert old in s
s=s.replace(old,"caps=[(10.55,18.6,'Five habits at 50 add up to 14 years.',{7,8})]")
s=s.replace("caption(['The','Longevity','Masterclass','of','the','Year'],{3,4,5},54,1080,'Regular')","caption('Learn to age slower from the 2nd slowest-aging human on Earth.'.split(),{6,7,8,9,10},54,1080,'Regular')")
s=s.replace("caption(['The','Longevity','Masterclass','of','the','Year'],{3,4,5},50,1080,'Regular')","caption('Learn to age slower from the 2nd slowest-aging human on Earth.'.split(),{6,7,8,9,10},50,1080,'Regular')")
s=s.replace('def strap(img,fmt):','def strap(img,fmt):\n    return img\ndef _old_strap(img,fmt):',1)
open(p,'w').write(s); compile(s,p,'exec'); print('patched ok')
