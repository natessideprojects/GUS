from pathlib import Path
import hashlib,json,zipfile,shutil

ROOT=Path(__file__).resolve().parents[1]
assert 'onedrive' not in str(ROOT).lower()
OUT=ROOT/'releases'
sources=[('GUS-North-Georgia-Windows-Demo.zip',ROOT.parent/'C.L.I.V.E/outputs/GUS North Georgia Candidate 2026-11-04','GUS-North-Georgia-Demo'),('GUS-DIY-Windows-Demo.zip',ROOT.parent/'G.U.S. DIY/outputs/G.U.S. DIY Windows Candidate 2026-11-03','GUS-DIY-Demo')]
notice='''G.U.S. DEMO — TESTING ONLY — NOT A FULL RELEASE

These are complete demo app files, with known issues. Keep original documents and
backups. Do not rely on answers, maps or routes for emergency or safety decisions.
Windows: extract the ENTIRE ZIP, then open the top-level EXE inside the extracted
folder. Keep System and OWNER_FILES beside the launcher. Do not run inside the ZIP.
The North Georgia Android APK is a separate release download, not in this Windows ZIP.
DIY Android is unfinished and is not supplied.

The owner confirmed completion of the redistribution review on November 7, 2026.
Older preview statements in the retained app documentation describe earlier builds;
this download is now offered as a public testing demo, not a production release.
Retain all bundled third-party license notices, terms and attribution.
Full installation, known issues, support and contact: https://gusdrive.com/
'''
def sha(p):
 with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
manifest=[]
for name,source,folder in sources:
 assert not(source/'.BUILD_INCOMPLETE').exists()
 for rel in ['OWNER_FILES','System/user','System/user_data']:assert not any((source/rel).rglob('*'))
 entries=[]
 for line in(source/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
  digest,rel=line.split(None,1);p=(source/rel.strip()).resolve();assert p.is_relative_to(source.resolve())
  assert sha(p)==digest.lower(),rel
  if p.suffix.lower()!='.apk':entries.append((p,rel.strip()))
 target=OUT/name
 if not target.exists():
  print('Verified clean package; compressing '+name,flush=True)
  with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True)as z:
   for p,rel in entries:z.write(p,folder+'/'+rel)
   z.writestr(folder+'/DEMO-README.txt',notice)
   z.writestr(folder+'/SHA256SUMS.txt',(source/'SHA256SUMS.txt').read_text(encoding='utf-8'))
   z.writestr(folder+'/OWNER_FILES/',b'')
 with zipfile.ZipFile(target)as z:assert z.testzip() is None
 row=dict(file=name,bytes=target.stat().st_size,sha256=sha(target),extracted_bytes=sum(p.stat().st_size for p,_ in entries),files=len(entries))
 if target.stat().st_size>=2*1024**3:
  row['reassembled']=True
  with target.open('rb')as source_stream:
   for part in range(1,3):
    destination=OUT/(name+f'.{part:03d}')
    with destination.open('wb')as out:
     remaining=1900000000
     while remaining:
      block=source_stream.read(min(1048576,remaining))
      if not block:break
      out.write(block);remaining-=len(block)
    manifest.append(dict(file=destination.name,bytes=destination.stat().st_size,sha256=sha(destination)))
   assert not source_stream.read(1),'More than two parts required'
 manifest.append(row)
 (OUT/'downloads.json').write_text(json.dumps(manifest,indent=2))
 print('Archive verified: '+name,flush=True)
apk=sources[0][1]/'GUS North Georgia Android.apk';target=OUT/'GUS-North-Georgia-Android-v53.apk'
shutil.copyfile(apk,target);assert sha(target)=='0a484a7e3d4368ec5a186007ba52430c148bd95654906b8a451ccb3e1013374d'
manifest.append(dict(file=target.name,bytes=target.stat().st_size,sha256=sha(target)))
(OUT/'DEMO-README.txt').write_text(notice)
(OUT/'downloads.json').write_text(json.dumps(manifest,indent=2))
(OUT/'SHA256SUMS.txt').write_text(''.join(r['sha256']+'  '+r['file']+'\n'for r in manifest))
print(json.dumps(manifest),flush=True)
