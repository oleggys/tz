import hashlib
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import favicon
import requests
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from bookmarks_service.forms import AddBookmarkForm
from bookmarks_service.models import Bookmark

# @shared_task decorator used to define the function of the celery task
@shared_task
def parse_page(url):
    # load and save favicon
    icon = favicon.get(url)[0]
    response = requests.get(icon.url, stream=True)
    hashed_url = hashlib.md5(url.encode('utf-8'))
    icon_name = '{0}.{1}'.format(hashed_url.hexdigest(), icon.format)
    image_path = 'media/favicons/' + icon_name
    with open(image_path, 'wb') as image:
        for chunk in response.iter_content(1024):
            image.write(chunk)

    # load html from web page
    response = urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    head = soup.find("head")
    title, description = '', ''

    found_block = head.find("title")
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

    bookmark = Bookmark.objects.get(url=url)
    bookmark.favicon = icon_name
    bookmark.title = title
    bookmark.description = description
    bookmark.save()


def index(request):
    return render(request, 'index.html')


def link_list(request):
    args = {}
    args["links"] = []
    try:
        args["links"] = Bookmark.objects.all().filter(add_by_user=request.user)
    except ObjectDoesNotExist as e:
        pass
    return render(request, 'link_list.html', args)


def add_bookmark(request):
    args = {}
    if request.method == "POST":
        url = request.POST.get("url")
        user = request.user
        form = AddBookmarkForm(request.POST)
        try:
            bookmark = Bookmark.objects.get(url=url)
            assert (user not in bookmark.add_by_user.all())
            bookmark.add_by_user.add(user)
            bookmark.save()
            form = AddBookmarkForm()
        except ObjectDoesNotExist as e:
            if form.is_valid():
                form.save()
                form = AddBookmarkForm()
                bookmark = Bookmark.objects.get(url=url)
                bookmark.add_by_user.add(request.user)
                bookmark.save()
                parse_page.delay(url)
        except AssertionError as e:
            form.add_error("url", "You added this link yet")
    else:
        form = AddBookmarkForm()
    args["form"] = form
    return render(request, 'add_bookmark.html', args)
