"""Package a checksum-verified official Electron Windows runtime; no external browser."""
import argparse,hashlib,json,pathlib,shutil,struct,zipfile,re,subprocess
p=argparse.ArgumentParser();p.add_argument('runtime_dir',type=pathlib.Path);p.add_argument('output',type=pathlib.Path);a=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[1];meta=json.loads((a.runtime_dir/'runtime.json').read_text());runtime=a.runtime_dir/meta['filename']
assert hashlib.sha256(runtime.read_bytes()).hexdigest()==meta['sha256'],'Runtime checksum mismatch'
build=a.output.parent/'native-build'/'Riser-Studio-Windows'
if build.exists():shutil.rmtree(build)
build.mkdir(parents=True)
with zipfile.ZipFile(runtime) as z:z.extractall(build)
(build/'electron.exe').rename(build/'Riser-Studio.exe')
pe=(build/'Riser-Studio.exe').read_bytes();offset=struct.unpack_from('<I',pe,60)[0];assert pe[offset:offset+4]==b'PE\0\0' and struct.unpack_from('<H',pe,offset+4)[0]==0x8664
app=build/'resources'/'app';app.mkdir(parents=True)
for name in ['main.cjs','preload.cjs','package.json','Riser-Studio.ico']:shutil.copy2(root/'desktop'/name,app/name)
renderer=app/'renderer';renderer.mkdir()
html=(root/'dist'/'index.html').read_text()
csp="default-src 'self' data: blob:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src 'self' data:; img-src 'self' data: blob:; connect-src 'none'; object-src 'none'; frame-src 'none'; base-uri 'none'"
marker='<meta charset="utf-8">'
assert marker in html, 'Missing document charset marker'
html=html.replace(marker,marker+'\n<meta http-equiv="Content-Security-Policy" content="'+csp+'">',1)
assert html.index('http-equiv="Content-Security-Policy"') < html.index('<script>')
for script in re.findall(r'<script>([\s\S]*?)</script>',html):
 subprocess.run(['node','--check'],input=script,text=True,check=True,capture_output=True)
(renderer/'index.html').write_text(html)
shutil.copy2(root/'dist'/'font-licenses.txt',renderer/'font-licenses.txt')
shutil.copy2(root/'dist'/'xlsx-license.txt',renderer/'xlsx-license.txt')
(build/'resources'/'default_app.asar').unlink(missing_ok=True)
shutil.copy2(root/'desktop'/'USER-GUIDE.txt',build/'USER-GUIDE.txt')
shutil.copy2(root/'dist'/'manufacturer-data.json',build/'manufacturer-data.json')
(build/'README.txt').write_text('RISER STUDIO — WINDOWS DESKTOP\n\n1. Extract the entire ZIP into a folder on your Windows 10/11 64-bit PC.\n2. Double-click Riser-Studio.exe. Keep the other files and folders with it.\n\nThis is a standalone application; no browser, Node.js or internet connection is required.\nUse File > Save / Save As to save independent .riser project files.\nUse File > Open to reopen .riser projects or import older project HTML/JSON files.\nPDF, SVG and editable DXF export are available. DXF can be opened in AutoCAD.\n\nThis portable build is unsigned and has not been launch-tested on Windows.\nCable calculations and elevations require engineering review before construction.\n\nRuntime: Electron '+meta['version']+' (Windows x64).\nRuntime source: '+meta['download_url']+'\nRuntime SHA256: '+meta['sha256']+'\nElectron/Chromium and font licence notices are included.\n')
(build/'build-info.json').write_text(json.dumps({'runtime':meta,'renderer_sha256':hashlib.sha256(html.encode()).hexdigest()},indent=2))
a.output.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(a.output,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(build.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(build.parent))
with zipfile.ZipFile(a.output) as z:assert z.testzip() is None
print(json.dumps({'output':str(a.output),'size':a.output.stat().st_size,'sha256':hashlib.sha256(a.output.read_bytes()).hexdigest(),'files':len(list(build.rglob('*')))}))
