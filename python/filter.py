import json
import requests

url = 'http://backstage-api.npo.nl/v0'

s = requests.session()

data_filter = {
    "filters": {
        "Locations.Name": {
            "terms": ["Amsterdam"]
        }
    }
}

r = s.post(url + '/journalistiek/search', data=json.dumps(data_filter))
print json.dumps(r.json(), indent=4)
