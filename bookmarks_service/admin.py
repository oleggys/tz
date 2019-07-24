from django.contrib import admin
from bookmarks_service.models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    fields = ['favicon', 'title', 'url', 'description']


admin.site.register(Bookmark, BookmarkAdmin)