import subprocess,json,sys
h=sys.argv[1]; cut=sys.argv[2]; T=sys.argv[3]
r=subprocess.run(['ffmpeg','-hide_banner','-i',f'out/{h}.wav','-af','loudnorm=I=-14:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
j=json.loads(r[r.rindex('{'):r.rindex('}')+1])
af=f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,alimiter=limit=0.70:level=false,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo"
subprocess.run(['ffmpeg','-v','error','-y','-i',f'out/{h}.wav','-af',af,'-c:a','aac','-b:a','192k',f'out/{h}.m4a'])
for f in ('9x16','1x1'):
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'fin/{h}_{f}_v31.mp4','-i',f'end/ending_{f}.mp4','-i',f'out/{h}.m4a','-filter_complex',f'[0:v]trim=0:{cut},setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0,fps=24,format=yuv420p[v]','-map','[v]','-map','2:a','-c:v','libx264','-preset','veryfast','-crf','17','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','copy','-t',T,'-movflags','+faststart',f'fin/{h}_{f}_v32.mp4'])
print('DONE',h)
