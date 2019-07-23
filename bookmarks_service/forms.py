from django import forms
from bookmarks_service.models import Bookmark


class AddBookmarkForm(forms.ModelForm):

    class Meta:
        model = Bookmark
        fields = ('url', )
