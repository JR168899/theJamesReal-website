"""Upload only public content to the selected development branch; no subscriber reads.
Connection is accepted through hidden stdin and never saved or logged.
"""
import json,sys,termios,urllib.request,urllib.parse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist'
old=termios.tcgetattr(sys.stdin);new=list(old);new[3]&=~termios.ECHO;termios.tcsetattr(sys.stdin,termios.TCSANOW,new)
print('Ready for database connection on hidden stdin.',flush=True)
uri=sys.stdin.readline().strip();termios.tcsetattr(sys.stdin,termios.TCSANOW,old)
host=urllib.parse.urlparse(uri).hostname

def sql(query,params=[]):
 body=json.dumps({'query':query,'params':params}).encode();req=urllib.request.Request('https://'+host+'/sql',data=body,headers={'Content-Type':'application/json','Neon-Connection-String':uri,'Neon-Raw-Text-Output':'false','Neon-Array-Mode':'false'})
 try:
  with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
 except Exception as e:
  print('Database operation failed:',type(e).__name__,getattr(e,'code',''),flush=True)
  if hasattr(e,'read'):
   detail=e.read().decode()[:1200].replace(uri,'[redacted]');print(detail,flush=True)
  raise SystemExit(1)
# The migration is additive. Run statements separately using the documented HTTP query interface.
for statement in (ROOT/'migrations/001_prepared_content.sql').read_text().split(';'):
 if statement.strip():sql(statement)
rows=[]
for p in sorted((D/'data/english-levels').glob('*.json')):
 for level,unit in json.loads(p.read_text()).items():rows.append((p.stem,'english',level,unit))
for folder,kind in [('recipes-archive','recipes'),('english-archive','legacy_english'),('health-archive','health')]:
 for p in sorted((D/'data'/folder).glob('*.json')):rows.append((p.stem,kind,'',json.loads(p.read_text())))
for start in range(0,len(rows),20):
 batch=rows[start:start+20];params=[];values=[]
 for day,kind,level,payload in batch:
  raw=json.dumps(payload,ensure_ascii=False,separators=(',',':'));base=len(params);params.extend([day,kind,level,raw,hashlib.sha256(raw.encode()).hexdigest()]);values.append('('+','.join('$'+str(base+i)+('::jsonb' if i==4 else '') for i in range(1,6))+')')
 sql('INSERT INTO jamesreal_content.editions(edition_date,kind,level,payload,source_sha256) VALUES '+','.join(values)+' ON CONFLICT(edition_date,kind,level) DO UPDATE SET payload=EXCLUDED.payload,source_sha256=EXCLUDED.source_sha256 WHERE editions.source_sha256 IS DISTINCT FROM EXCLUDED.source_sha256',params)
 print('Saved public editions:',min(start+20,len(rows)),'/',len(rows),flush=True)
result=sql("SELECT kind,count(*)::int AS editions,min(edition_date)::text AS first_day,max(edition_date)::text AS last_day FROM jamesreal_content.editions GROUP BY kind ORDER BY kind")
(ROOT/'content/neon-sync-result.json').write_text(json.dumps(result,indent=2));print('Public content synchronization complete.',flush=True)
