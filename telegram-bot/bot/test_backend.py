import sys
import traceback
import requests
from bot.config import settings

print('Using BACKEND_URL=', settings.backend_url)
print('HTTP_PROXY=', settings.http_proxy)
print('HTTPS_PROXY=', settings.https_proxy)

urls = [settings.backend_url + '/docs', settings.backend_url + '/']
proxies = None
if settings.http_proxy or settings.https_proxy:
    proxies = {}
    if settings.http_proxy:
        proxies['http'] = settings.http_proxy
    if settings.https_proxy:
        proxies['https'] = settings.https_proxy
    print('Using proxies:', proxies)
else:
    print('No proxies configured')

session = requests.Session()
# Do not use environment proxies (some systems have HTTP_PROXY set and cause 502)
session.trust_env = False
for u in urls:
    try:
        print('\nRequesting', u)
        if proxies:
            r = session.get(u, timeout=5, proxies=proxies)
        else:
            r = session.get(u, timeout=5)
        print('Status:', r.status_code)
        print('Content-length:', len(r.text))
    except Exception as e:
        print('Error requesting', u)
        traceback.print_exc()
        sys.exit(1)

print('\nTest finished')

# Extra raw HTTP test using http.client to see raw response
import http.client
from urllib.parse import urlparse

u = settings.backend_url
parsed = urlparse(u)
host = parsed.hostname
port = parsed.port or (443 if parsed.scheme == 'https' else 80)
print('\nRaw HTTP test to', host, port)
try:
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request('GET', '/')
    resp = conn.getresponse()
    print('Raw status:', resp.status)
    print('Raw reason:', resp.reason)
    print('Raw headers:')
    for k, v in resp.getheaders():
        print(f'  {k}: {v}')
    body = resp.read()
    print('Raw body length:', len(body))
    print('Raw body (first 200 bytes):', body[:200])
    conn.close()
except Exception:
    print('Raw HTTP test failed')
    traceback.print_exc()
