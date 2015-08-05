import json
import requests
from pprint import pprint

NPO_BACKSTAGE_BASE_URL = 'http://backstage-api.npo.nl'
NPO_BACKSTAGE_ENDPOINT_SEARCH = '/v0/search'

SEARCH_DATA = {
    "query": "leenstelsel",
    "size": 5
}

# It is a good idea to start a requests session if you are going to
# make more than one call to the API as it will keep the connection
# open
session = requests.session()

response = session.post(
    NPO_BACKSTAGE_BASE_URL + NPO_BACKSTAGE_ENDPOINT_SEARCH,
    data=json.dumps(SEARCH_DATA)
)

# Print each returned item
for item in response.json()['hits']['hits']:
    pprint(item)
    print '\n\n'
