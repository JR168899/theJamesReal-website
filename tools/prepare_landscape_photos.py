"""Prepare licensed landscape assets. Uses cached source originals when available."""
from pathlib import Path
import json,urllib.request,concurrent.futures,io
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist';p=ROOT/'content/photo-catalog.json';catalog=json.loads(p.read_text());rawdir=ROOT.parent.parent/'work/english-landscape-originals';rawdir.mkdir(parents=True,exist_ok=True)
def prepare(row):
 key,c=row;pid=c['id'];raw=rawdir/f'{pid}.jpg'
 if not raw.exists():
  req=urllib.request.Request(f'https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=1200',headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=60) as r:raw.write_bytes(r.read())
 im=Image.open(raw).convert('RGB');w,h=im.size
 if w<=h:return key,{'rejectedOrientation':[w,h]}
 im=ImageOps.fit(im,(644,285),method=Image.Resampling.LANCZOS,centering=(.5,c.get('focalY',.45)))
 for quality in range(78,39,-4):
  b=io.BytesIO();im.save(b,format='JPEG',quality=quality,optimize=True)
  if b.tell()<=20000:break
 out=D/c['asset'];out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b.getvalue());c.update(originalDimensions=[w,h],dimensions=[644,285],bytes=b.tell(),quality=quality,landscape=True)
 return key,c
def safe(row):
 try:return prepare(row)
 except Exception as e:return row[0],{'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:results=dict(ex.map(safe,catalog.items()))
rejected={k:v for k,v in results.items() if 'rejectedOrientation' in v or 'error' in v}
for k,v in results.items():
 if k not in rejected:catalog[k]=v
p.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n');print('Prepared',len(catalog)-len(rejected),'landscape scenes; rejected:',rejected)
