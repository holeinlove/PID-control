"""Package only the reviewed upload scope. Does not contact GitHub."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import hashlib, json, zipfile, re
root=Path(__file__).resolve().parents[1]
def read_json(name):return json.loads((root/'evidence'/name).read_text(encoding='utf-8-sig'))
for report in ['numerical-tests.json','browser-tests.json','browser-recording-tests.json']:
 data=read_json(report)
 assert all(row['status']=='PASS' for row in data['results']),report
for report in ['endurance-tests.json','visibility-tests.json']:assert read_json(report)['status']=='PASS',report
assert (root/'PID control Cart-Pole.html').read_bytes()==(root/'index.html').read_bytes()
log=(root/'ITERATION-AND-ACCEPTANCE.md').read_text(encoding='utf-8-sig')
assert len(re.findall(r'^\| A\d\d \|',log,re.M))==24
assert '| A22 | 待測' in log
files=[root/n for n in ['PID control Cart-Pole.html','index.html','PID-control-Cart-Pole-spec.md','ui-reference.svg','ITERATION-AND-ACCEPTANCE.md']]
files+=sorted(p for p in (root/'tests').iterdir() if p.is_file())
files+=sorted(p for p in (root/'evidence').iterdir() if p.is_file())
entries=[{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
manifest={'preparedAt':datetime.now(timezone(timedelta(hours=8))).isoformat(),'repository':'https://github.com/holeinlove/PID-control.git','targetBranch':'main','authorization':'PENDING - no upload or publication has occurred','changes':'New files in currently empty repository; no existing files replaced','pagesScope':{'currentHasPages':False,'requestEnable':True,'sourceBranch':'main','sourcePath':'/','effect':'Enable first GitHub Pages publication; subsequent pushes to this source trigger automatic rebuild','workflowFilesAdded':False},'manifestFile':'upload-manifest.json','note':'This manifest is itself included in requested upload scope; its own hash is intentionally omitted. Raw disturbance-frames PNGs are local-only.','files':entries}
manifest_path=root/'upload-manifest.json'
manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
archive=root.parent/'PID-control-review.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[manifest_path]:z.write(p,p.relative_to(root).as_posix())
with zipfile.ZipFile(archive) as z:
 for entry in entries:assert hashlib.sha256(z.read(entry['path'])).hexdigest()==entry['sha256'],entry['path']
print(json.dumps({'archive':str(archive),'filesIncludingManifest':len(entries)+1,'archiveBytes':archive.stat().st_size,'htmlSha256':hashlib.sha256((root/'index.html').read_bytes()).hexdigest(),'A24':'Local files, complete 24-row acceptance record and ZIP verified; A22 pending deployment'},ensure_ascii=False,indent=2))
