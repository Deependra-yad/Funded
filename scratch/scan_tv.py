import urllib.request

req = urllib.request.Request(
    'https://scanner.tradingview.com/global/scan',
    data=b'{"columns":["name","description","exchange"],"filter":[{"left":"exchange","operation":"equal","right":"BINGX"}]}',
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
)
try:
    res = urllib.request.urlopen(req)
    print(res.read().decode('utf-8'))
except Exception as e:
    print(e)

