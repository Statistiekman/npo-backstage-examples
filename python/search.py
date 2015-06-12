import simplejson as json
import requests
import pprint

NPO_BACKSTAGE_BASE_URL = 'http://backstage-api.openstate.eu'
NPO_BACKSTAGE_ENDPOINT_SEARCH = '/v0/search'

SEARCH_DATA = {
    "query": "leenstelsel",
    "size": 5
}

r = requests.post(
    NPO_BACKSTAGE_BASE_URL +
    NPO_BACKSTAGE_ENDPOINT_SEARCH,
    data=json.dumps(SEARCH_DATA)
    )

for item in json.loads(r.text)['hits']['hits']:
    d = item['_source']
    # Datum<tab>ID<tab>Titel
    print "%s\t%s\t%s" % (d['date'], item['_id'], d['title'])
