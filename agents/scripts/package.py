from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1]
dist=root/'dist';dist.mkdir(exist_ok=True)
def pack(name,files,base):
 with zipfile.ZipFile(dist/name,'w',zipfile.ZIP_DEFLATED) as z:
  for p in files:
   if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc': z.write(p,p.relative_to(base))
skill=root/'skills/job-search-jev'
pack('job-search-jev-claude.zip',skill.rglob('*'),skill.parent)
pack('jobscout-chatgpt-plugin.zip',[root/'plugin.json',*skill.rglob('*')],root)
print('Created Claude skill and ChatGPT plugin ZIPs')
