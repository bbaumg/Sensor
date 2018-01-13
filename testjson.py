import requests
url = 'https://status.github.com/api/status.json'
resp = requests.get(url)
o = resp.json()
print(o['status'])
for key, value in o.items():
	print(key)
	print(value)
