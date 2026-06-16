import urllib.request, urllib.parse, re, sys
from urllib.error import URLError, HTTPError
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
root = 'https://krupalipatiwala12.github.io/ShadowFox/BakersStudio/'
print('Fetching', root)
try:
    data=urllib.request.urlopen(root)
    html=data.read().decode('utf-8', errors='replace')
    print('Index status', data.getcode(), 'content-type', data.getheader('Content-Type'))
except Exception as e:
    print('Failed to fetch index:', e)
    sys.exit(1)
refs=set()
for m in re.findall(r'href=["\']([^"\']+)["\']', html):
    if not re.match(r'^(https?:|mailto:|tel:|#)', m): refs.add(m)
for m in re.findall(r'src=["\']([^"\']+)["\']', html):
    if not re.match(r'^(https?:|data:|mailto:|tel:|#)', m): refs.add(m)
# add CSS assets inside linked CSS files
print('\nFound', len(refs), 'references in index.html')
results=[]
for r in sorted(refs):
    url = urllib.parse.urljoin(root, r)
    try:
        resp=urllib.request.urlopen(url)
        code=resp.getcode()
        ctype=resp.getheader('Content-Type')
        results.append((r, url, code, ctype))
        print(r, '->', code, ctype)
        if r.endswith('.css'):
            css=resp.read().decode('utf-8', errors='replace')
            for mm in re.findall(r'url\(["\']?([^"\')]+)["\']?\)', css):
                if not re.match(r'^(https?:|data:)', mm):
                    murl=urllib.parse.urljoin(url, mm)
                    try:
                        r2=urllib.request.urlopen(murl)
                        print('  css asset', mm, '->', r2.getcode(), r2.getheader('Content-Type'))
                        results.append((mm, murl, r2.getcode(), r2.getheader('Content-Type')))
                    except HTTPError as he:
                        print('  css asset', mm, 'HTTP', he.code)
                        results.append((mm, murl, he.code, None))
                    except Exception as e:
                        print('  css asset', mm, 'ERR', e)
                        results.append((mm, murl, 'ERR', str(e)))
    except HTTPError as he:
        print(r, '-> HTTP', he.code)
        results.append((r, url, he.code, None))
    except URLError as ue:
        print(r, '-> URLERR', ue)
        results.append((r, url, 'URLERR', str(ue)))
    except Exception as e:
        print(r, '-> ERR', e)
        results.append((r, url, 'ERR', str(e)))

# summarize failures
fails=[t for t in results if not (isinstance(t[2], int) and 200<=t[2]<400)]
print('\nSummary: {} total refs, {} failures'.format(len(results), len(fails)))
for f in fails:
    print('FAIL:', f)

# compare with local files
import pathlib
root_local=pathlib.Path(__file__).resolve().parent
local_files={str(p.relative_to(root_local)).replace('\\','/') for p in root_local.rglob('*') if p.is_file()}
print('\nLocal files count:', len(local_files))
# list missing paths that failed
for r,url,code,ct in fails:
    # make relative path
    rel=r.lstrip('/')
    print('Checking local match for', rel)
    matches=[x for x in local_files if x.lower().endswith(rel.lower()) or x.lower()==rel.lower()]
    print(' Local matches (ignore-case):', matches[:10])
print('\nRemote audit complete')
