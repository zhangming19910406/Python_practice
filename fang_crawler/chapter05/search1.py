# usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import string

template_url = 'http://example.webscraping.com/places/ajax/search.json?&search_term={}&page_size=10&page={}'
countries = set()

for letter in string.ascii_lowercase:
    page = 0
    while True:
        html = D(template_url.format(page, letter))
        try:
            ajax = json.loads(html)
        except ValueError as e:
            print(e)
            ajax = None
        else:
            for record in ajax['records']:
                countries.add(record['country'])
        page += 1
        if ajax is None or page >= ajax['num_pages']:
            break
open('countries.txt', 'w').write('\n'.join(sorted(countries)))
