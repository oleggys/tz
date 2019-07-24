import favicon
import requests
import json
import hashlib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from tz import app_test


# @app_test.task decorator used to define the function of the celery task
@app_test.task
def parse_page(url):
    # load and save favicon
    icon = favicon.get(url)[0]

    # load html from web page
    response = urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    head = soup.find("head")
    title, description = '', ''

    found_block = head.find("title")
    if found_block is None:
        title = found_block.text

    found_block = head.find("meta", {"property": "og:title"})
    if found_block is None:
        found_block = head.find("meta", {"name": "title"})
    if found_block is None:
        found_block = head.find("meta", {"name": "twitter:title"})

    if found_block is not None:
        title = found_block.attrs['content']

    found_block = head.find("meta", {"name": "description"})
    if found_block is None:
        found_block = head.find("meta", {"property": "og:description"})
    if found_block is None:
        found_block = head.find("meta", {"name": "twitter:description"})

    if found_block is not None:
        description = found_block.attrs['content']

    found_block = head.find("script", type="application/ld+json")
    if found_block is not None:
        datastore = json.loads(found_block.text or '{}')
        if title == '':
            try:
                title = datastore["title"]
            except KeyError as e:
                title = ''
        if description == '':
            try:
                description = datastore["description"]
            except KeyError as e:
                description = ''

    from bookmarks_service.models import Bookmark
    bookmark = Bookmark.objects.get(url=url)
    bookmark.favicon = icon.url
    bookmark.title = title
    bookmark.description = description
    bookmark.save()
