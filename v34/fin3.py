import subprocess,json,sys
h=sys.argv[1]; cut=sys.argv[2]; T=sys.argv[3]; sh=float(sys.argv[4])
r=subprocess.run(['ffmpeg','-hide_banner','-i',f'out/{h}.wav','-af','loudnorm=I=-14:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
j=json.loads(r[r.rindex('{'):r.rindex('}')+1])
af=f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,alimiter=limit=0.70:level=false,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo"
subprocess.run(['ffmpeg','-v','error','-y','-i',f'out/{h}.wav','-af',af,'-c:a','aac','-b:a','192k',f'out/{h}.m4a'])
for f in ('9x16','1x1'):
    body=f'hb/v24_{f}.video.mp4' if h=='ad1' else f'out/{h}_{f}.video.mp4'
    a,b=38.875-sh,39.705-sh
    o28=f"[v1][3:v]overlay=enable='between(t,17.167,19.82)'[v2]" if h=='ad1' else "[v1]null[v2]"
    fc=f"[0:v][2:v]overlay=enable='between(t,{a:.3f},{b:.3f})':shortest=1[v1];{o28};[v2]trim=0:{cut},setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0,fps=24,format=yuv420p[v]"
    subprocess.run(['ffmpeg','-v','error','-y','-i',body,'-i',f'end/ending_{f}.mp4','-loop','1','-i',f'cf/cas_{f}.png','-loop','1','-i',f'cf/c28_{f}.png','-i',f'out/{h}.m4a','-filter_complex',fc,'-map','[v]','-map','4:a','-c:v','libx264','-preset','veryfast','-crf','17','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','copy','-t',T,'-movflags','+faststart',f'fin/{h}_{f}_v34.mp4'])
print('DONE',h)
