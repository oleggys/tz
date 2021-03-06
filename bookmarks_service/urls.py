from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('list/', views.link_list, name="link_list"),
    path('add_bookmark/', views.add_bookmark, name="add_bookmarks"),
]