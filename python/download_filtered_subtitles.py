#!/usr/bin/env python

import codecs
import os
import requests

# This program downloads and saves subtitles for the specified programs
# by filtering on the metadata index and retrieving the subtitles from
# the tt888 index

# Main directory which will hold the downloaded data
data_dir = 'npo_backstage_subtitles/'

# The programs for which subtitles will be downloaded
programs = ['EenVandaag', 'Nieuwsuur']

# Base URL of the NPO Backstage API
base_url = 'http://backstage-api.npo.nl/v0'

# The number of results per page when filtering the metadata index
step_size = 100

# We use the package 'requests' to download the data
session = requests.session()

for program in programs:
    program_dir = data_dir + program

    print 'Downloading subtitles for program "%s" to %s' % (
        program,
        program_dir
    )

    # Create the directory if it does not exist
    if not os.path.exists(program_dir):
        os.makedirs(program_dir)

    # Keep downloading
    metadata_page = 0
    subtitle_count = 0
    while True:
        # Prepare the request
        from_item = step_size * metadata_page
        params = (
            '{"filters": {"title": {"terms": ["%s"]}}, '
            '"size": %s, "from": %s}' % (program, step_size, from_item)
        )
        metadata_url = '%s/metadata/search' % (base_url)

        print (
            '\nDownloading metadata, page %s with %s items per page by '
            'POSTing to URL %s with body %s' % (
                str(metadata_page + 1),
                str(step_size),
                metadata_url,
                params
            )
        )

        # Download the data via a POST request
        result = session.post(
            metadata_url,
            data=params
        )

        # The API returns its data as JSON, so extract the JSON from the
        # result
        metadata_items = result.json()

        # If 'hits' contains no items, then there are no items left so
        # stop downloading and break out of the while loop
        if len(metadata_items['hits']['hits']) == 0:
            print 'No more metadata items left for program %s\n\n' % (program)
            break

        # Process each metadata item
        for item in metadata_items['hits']['hits']:
            # Check if the metadata specifies that this item contains
            # tt888 (i.e., subtitles)
            if item['_source']['tt888'] == 'ja':
                prid = item['_source']['prid']
                subtitle_url = '%s/tt888/%s' % (base_url, prid)
                # Download the subtitle using the item's 'prid' (i.e.,
                # PRogram ID) via a GET request
                subtitle_result = session.get(subtitle_url)
                subtitle_item = subtitle_result.json()

                # Check if there really is a subtitle
                if 'subtitle' in subtitle_item:
                    subtitle_count += 1
                    # Save the subtitle
                    print (
                        'Downloaded subtitle (#%s) of prid %s using GET on '
                        'URL %s' % (subtitle_count, prid, subtitle_url)
                    )
                    with codecs.open('%s/%s.json' % (program_dir, prid),
                                     'w', 'utf-8') as OUT:
                        OUT.write(subtitle_item['subtitle'])
                else:
                    print (
                        'Found no subtitle for prid %s on %s' % (
                            prid,
                            subtitle_url
                        )
                    )

        # Increase the page counter to download the next page
        metadata_page += 1
