from django.contrib import admin
from bookmarks_servis.models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    fields = ["title", 'url', 'get_domain']


admin.site.register(Bookmark)