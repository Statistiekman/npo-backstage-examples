NPO Backstage Examples
======================
This repository contains example code for data from the [NPO Backstage](http://www.npo.nl/specials/backstage) API. In the ``python`` folder we currently have the following examples:
- ``simple_search.py``: simple example of how to search the API using Python
- ``facet.py``: shows how to apply facetting
- ``filter.py``: shows how to apply filtering
- ``download_filtered_subtitles.py``: filters on the ``metadata`` index for the specified programs (default 'Nieuwsuur' and 'EenVandaag') and downloads their subtitles if available from the ``tt888`` index
- ``generate_wordcloud.py``: a fun example of what you can do with the subtitle texts; after you downloaded subtitles using ``download_filtered_subtitles.py``, use this progam to generate word clouds using Parsimonious Language Models, which will retrieve the words which are most distinctive for each program compared to the other program(s) (default 'Nieuwsuur' and 'EenVandaag')

Problems with the API and feature requests can also be reported here on the [Issues page](https://github.com/openstate/npo-backstage-examples/issues).

NPO Backstage is an initiative of [NPO](http://www.npo.nl) in collaboration with [Open State Foundation](http://www.openstate.eu).

Links
-----
- [NPO Backstage documentation](http://backstage-docs.npo.nl): `must-read(!)`, contains amongst others a quickstart guide on how to use the API, descriptions of all API functionalities and explanation of all fields of each available dataset/index)
- [@NPOBackstage on Twitter](https://twitter.com/NPOBackstage)

License
--------
This NPO Backstage API example code is licensed under CC0.<br>
Please keep in mind that this license does not apply to the content of the API.
