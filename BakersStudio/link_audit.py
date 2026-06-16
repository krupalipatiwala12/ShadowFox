import pathlib
import re
root = pathlib.Path(__file__).resolve().parent
files = {str(p.relative_to(root)).replace('\\','/') for p in root.rglob('*') if p.is_file()}
missing = []
for p in root.rglob('*'):
    if p.suffix.lower() not in {'.html', '.css', '.js'}:
        continue
    text = p.read_text(encoding='utf-8', errors='ignore')
    refs = []
    if p.suffix.lower() == '.html':
        refs.extend(re.findall(r'href=["\']([^"\']+)["\']', text))
        refs.extend(re.findall(r'src=["\']([^"\']+)["\']', text))
    if p.suffix.lower() == '.css':
        refs.extend(re.findall(r'url\(["\']?([^"\')]+)["\']?\)', text))
    # ignore external URLs and JS template placeholders like ${...}
    refs = [r for r in refs if not re.match(r'^(https?:|data:|mailto:|tel:|#)', r) and '${' not in r]
    for r in refs:
        rpath = r[1:] if r.startswith('/') else r
        cand = (p.parent / rpath).resolve()
        try:
            rel = str(cand.relative_to(root)).replace('\\','/')
        except ValueError:
            rel = str(cand)
        if rel not in files:
            lower_matches = [x for x in files if x.lower() == rel.lower()]
            missing.append((str(p.relative_to(root)), r, rel, lower_matches[:5]))
print('FOUND', len(missing), 'MISSING REFERENCES')
for f, r, rel, lower in missing:
    print(f, '->', r, 'resolved as', rel, 'lower matches', lower)
