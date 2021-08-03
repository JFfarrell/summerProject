import urllib.parse
import urllib.error
import requests
import json
import config


headers = {
        # Request headers
        'Cache-Control': 'no-cache',
        'x-api-key': config.apikey,
    }

params = urllib.parse.urlencode({
})

gtfs = 'https://gtfsr.transportforireland.ie/v1/?format=json'
r = requests.get(gtfs, params=params, headers=headers)
data = json.loads(r.content)
print(data)