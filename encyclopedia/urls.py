from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<str:title>/", views.entry, name="entry"),
    path("entry/", views.search, name="search"),
    path("newpage/", views.newpage, name="newpage"),
    path("editpage/<str:title>/", views.editpage, name="editpage"),
    path("random/", views.randompage, name="random"),
]
