import json
import requests

url = 'http://backstage-api.npo.nl/v0'

s = requests.session()

# Retrieve the first 250 facets and retrieve 0 normal search results so
# the output will only show facets
data_facet = {
    "facets": {
        "Locations.Name": {"size": 250}
    },
    "size": 0
}

r = s.post(url + '/journalistiek/search', data=json.dumps(data_facet))
print json.dumps(r.json(), indent=4)
