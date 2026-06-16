import shutil, pathlib, zipfile
root = pathlib.Path(__file__).resolve().parent
src = root / 'Bakery.jpg'
dst = root / 'images' / 'bakery.jpg'
if src.exists():
    shutil.copy2(src, dst)
    print('Copied', src.name, '->', dst)
else:
    print('Source not found:', src)
zipf = root / 'BakersStudio-deploy.zip'
with zipfile.ZipFile(zipf, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in root.rglob('*'):
        if p.is_file():
            z.write(p, arcname=str(p.relative_to(root)))
print('Created zip:', zipf.name)
