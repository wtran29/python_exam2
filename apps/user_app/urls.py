from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^main$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^dashboard$', views.dashboard),
	url(r'^delete/(?P<item_id>\d+)$', views.delete),
	url(r'^remove/(?P<item_id>\d+)$', views.remove),
	url(r'^create_form$', views.create_form),
	url(r'^wish_items/create$', views.create),
	url(r'^wish_items/(?P<item_id>\d+)$', views.update),
	url(r'^show/(?P<item_id>\d+)$', views.display),
]