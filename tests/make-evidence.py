from PIL import Image
from pathlib import Path
import json
root=Path.cwd()
frames=sorted((root/'evidence'/'disturbance-frames').glob('*.png'))
measure=json.loads((root/'evidence'/'disturbance-measurements.json').read_text(encoding='utf-8'))
images=[]
for frame in frames:
 im=Image.open(frame).convert('RGB')
 images.append(im.resize((896,round(im.height*896/im.width))))
durations=[max(60,round((measure[i+1]['t']-measure[i]['t'])*1000)) for i in range(len(measure)-1)]+[500]
images[0].save(root/'evidence'/'manual-disturbance.gif',save_all=True,append_images=images[1:],duration=durations,loop=0,optimize=True)
for width in [320,768,1280]:
 im=Image.open(root/'evidence'/f'layout-{width}.png')
 im.crop((0,0,width,min(1000,im.height))).save(root/'evidence'/f'layout-{width}-top.png')
 if width==320:
  im.crop((0,im.height-1150,width,im.height)).save(root/'evidence'/'layout-320-teaching.png')
print('GIF made from actual screenshot frames; timing follows recorded simulation timestamps')
