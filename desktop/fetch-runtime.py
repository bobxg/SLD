"""Fetch the pinned official runtime; verify before packaging."""
import hashlib,json,pathlib,sys,urllib.request
out=pathlib.Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
meta={'version':'44.9.2','filename':'electron-v44.9.2-win32-x64.zip','sha256':'1a9ed7f4e70291c95ed9479d7fcd384a2d9cf062e5fb7ce846b119c7c63036c3','download_url':'https://github.com/electron/electron/releases/download/v44.9.2/electron-v44.9.2-win32-x64.zip'}
p=out/meta['filename']
urllib.request.urlretrieve(meta['download_url'],p)
if hashlib.sha256(p.read_bytes()).hexdigest()!=meta['sha256']:
 p.unlink();raise SystemExit('Runtime checksum mismatch')
(out/'runtime.json').write_text(json.dumps(meta,indent=2))
print('Official Windows runtime verified')
