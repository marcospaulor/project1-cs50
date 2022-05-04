'''
    URLS determine the URL structure of the website.
    Where the URL calls a view function.
'''
from django.urls import path

from . import views

urlpatterns = [
    # Path to the home page
    path("", views.index, name="index"),
    # Path to the page of an entry
    path("wiki/<str:entry>", views.entry, name="entry"),
    # Path to the search page
    path("search", views.search, name="search"),
    # Path to the page to create new entries
    path("create", views.create, name="create"),
    # Path to the page to edit an entry
    path("edit/<str:entry>", views.edit, name="edit"),
    # Path to a random page
    path("random", views.random, name="random"),
]
