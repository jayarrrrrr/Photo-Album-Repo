import urllib.request, sys
url='http://127.0.0.1:8000/accounts/login/?next=/albums/create/'
try:
    r=urllib.request.urlopen(url)
    print('STATUS', r.status)
    data=r.read(4000).decode('utf-8', errors='replace')
    print(data)
except Exception as e:
    print('ERROR', e)
    sys.exit(1)
