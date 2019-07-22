from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import URLValidator
from django.shortcuts import render
import asyncio
from bs4 import BeautifulSoup
from bookmarks_servis.forms import AddBookmarkForm
from bookmarks_servis.models import Bookmark

loop = asyncio.get_event_loop()


def parse_page(url):
    pass


def index(request):
    return render(request, 'index.html')


@login_required(redirect_field_name='index')
def link_list(request):
    args = {}
    args["links"] = []
    try:
        args["links"] = Bookmark.objects.get(add_by_user=request.user)
    except ObjectDoesNotExist as e:
        pass
    return render(request, 'link_list.html', args)


@login_required(redirect_field_name='index')
def add_bookmark(request):
    args = {}
    form = AddBookmarkForm()
    args["form"] = form
    return render(request, 'add_bookmark.html', args)


def add_bookmark_post_request(request):
    if request.method == "POST":
        args = {}
        form = AddBookmarkForm(request.POST)
        args["form"] = form
        if form.is_valid():
            form.save()
            loop.run_in_executor(None, parse_page, request.POST.get("url"))
            form.clean()
            args["added"] = True
            args["form"] = form
        return render(request, 'add_bookmark.html', args)
    else:
        return None