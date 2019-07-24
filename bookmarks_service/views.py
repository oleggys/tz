from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from bookmarks_service import tasks
from bookmarks_service.forms import AddBookmarkForm
from bookmarks_service.models import Bookmark


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
                tasks.parse_page.delay(url)
        except AssertionError as e:
            form.add_error("url", "You added this link yet")
    else:
        form = AddBookmarkForm()
    args["form"] = form
    return render(request, 'add_bookmark.html', args)
