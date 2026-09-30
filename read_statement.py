"""Prints the plain-text statement of given slugs (from specs.json)."""
import html
import re
import sys

import json
specs = json.load(open('specs.json', encoding='utf-8'))
for slug in sys.argv[1:]:
    c = (specs.get(slug) or {}).get('content') or ''
    txt = re.sub(r'<sup>', '^', c)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    txt = re.sub(r'[ \t]+', ' ', txt)
    txt = re.sub(r'\n\s*\n+', '\n', txt)
    print('=' * 78)
    print(slug.upper())
    print(txt.strip()[:1800])
