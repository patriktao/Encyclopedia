from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/create", views.create, name="create"),
    path("wiki/randompage", views.randompage, name="randompage"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/search", views.search, name="search"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
]
