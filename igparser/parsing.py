import re, json

def sorting(func, data):
	data = map(func, data)
	data = list(filter(lambda x: x.id != "", data))
	return data

def get_sharedData(html, decode = True):
	data = re.search(r'window._sharedData = (.+);</script>', html)	
	if not data:
		return

	if decode:
		return json.loads(data.group(1))
	else:
		return data.group(1)

def get_dataLoaded(html):
	data = re.search(r"window.__additionalDataLoaded\W'feed',(.+)\W;</script>", html)
	if not data:
		return

	return json.loads(data.group(1))