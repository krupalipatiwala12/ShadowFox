import urllib.request, urllib.parse, re
from urllib.error import URLError, HTTPError
import sys
root='http://localhost:8000'
print('Fetching', root+'/index.html')
try:
    data=urllib.request.urlopen(root+'/index.html')
    html=data.read().decode('utf-8', errors='replace')
    print('Index status', data.getcode(), 'content-type', data.getheader('Content-Type'))
except Exception as e:
    print('Failed to fetch index:', e)
    sys.exit(1)
refs=set()
# find links
for m in re.findall(r'href=["\']([^"\']+)["\']', html):
    if not re.match(r'^(https?:|mailto:|tel:|#)', m): refs.add(m)
for m in re.findall(r'src=["\']([^"\']+)["\']', html):
    if not re.match(r'^(https?:|data:|mailto:|tel:|#)', m): refs.add(m)
# also css url() from linked css later
print('\nFound', len(refs), 'references in index.html')
for r in sorted(refs):
    url = urllib.parse.urljoin(root + '/', r)
    try:
        resp=urllib.request.urlopen(url)
        code=resp.getcode()
        ctype=resp.getheader('Content-Type')
        print(r, '->', url, code, ctype)
        if r.endswith('.css'):
            css=resp.read().decode('utf-8', errors='replace')
            # find url() inside css
            for mm in re.findall(r'url\(["\']?([^"\')]+)["\']?\)', css):
                if not re.match(r'^(https?:|data:)', mm):
                    murl=urllib.parse.urljoin(url, mm)
                    try:
                        r2=urllib.request.urlopen(murl)
                        print('  css asset', mm, '->', r2.getcode(), r2.getheader('Content-Type'))
                    except Exception as e:
                        print('  css asset', mm, 'FAILED ->', e)
    except HTTPError as he:
        print(r, '->', url, 'HTTP', he.code)
    except URLError as ue:
        print(r, '->', url, 'URLERR', ue)
    except Exception as e:
        print(r, '->', url, 'ERR', e)
print('\nAudit complete')
