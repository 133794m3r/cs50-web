from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
	path("wiki/<str:page>",views.show_page,name='show_page'),
	path("search/<str:page>",views.search_page,name="search_page"),
	path("search",views.search_page,name="search_page"),
	path("random",views.random_page,name="random_page"),
	path("edit/<str:name>",views.edit_page,name="edit"),
	path("new",views.new_page,name="new")
]
