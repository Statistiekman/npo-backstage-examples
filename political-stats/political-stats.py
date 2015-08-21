#!/usr/bin/env python

import sys
import os
import re
import json
from pprint import pprint

import requests
from BeautifulSoup import BeautifulSoup

NPO_BACKSTAGE_BASE_URL = 'http://backstage-api.npo.nl'
NPO_BACKSTAGE_ENDPOINT_SEARCH = '/v0/search'

def get_politicians():
    url = u'http://www.tweedekamer.nl/kamerleden/alle_kamerleden'
    resp = requests.get(url)
    if resp.status_code != 200:
        return None

    soup = BeautifulSoup(resp.content)

    politicians = []
    for row in soup.findAll('div', 'member-info', recursive=True):
        politician = {
            'name': row.find('h2').text,
            'party': row.find('img')['alt'].split(u' ')[-1].replace(
                u'(', u'').replace(u')', u'')
        }
        politicians.append(politician)
    return politicians

def get_party_count(party, session):
    SEARCH_DATA = {
        "query": party,
        "size": 20
    }

    response = session.post(
        NPO_BACKSTAGE_BASE_URL + NPO_BACKSTAGE_ENDPOINT_SEARCH,
        data=json.dumps(SEARCH_DATA)
    )

    return response.json()['hits'].get('total', 0)

def get_politician_count(politician, session):
    SEARCH_DATA = {
        "query": politician['name'],
        "size": 20
    }

    response = session.post(
        NPO_BACKSTAGE_BASE_URL + NPO_BACKSTAGE_ENDPOINT_SEARCH,
        data=json.dumps(SEARCH_DATA)
    )

    return response.json()['hits'].get('total', 0)

def run(argv):
    politicians = get_politicians()
    parties = list(set([p['party'] for p in politicians]))
    pprint(politicians)
    pprint(parties)

    # It is a good idea to start a requests session if you are going to
    # make more than one call to the API as it will keep the connection
    # open
    session = requests.session()

    party_counts = [
        {'party': p, 'count': get_party_count(p, session)} for p in parties]
    pprint(party_counts)

    politician_counts = [
        {'politician': p, 'count': get_politician_count(p, session)} for p in politicians]
    pprint(politician_counts)

    return 0

if __name__ == '__main__':
    sys.exit(run(sys.argv))
