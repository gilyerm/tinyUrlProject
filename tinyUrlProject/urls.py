from django.urls import path, re_path

from tinyUrl import views

urlpatterns = [
    path('create', views.create, name='create'),
    re_path(r'^s/(?P<short_url>.*)?$', views.redirect, name='redirect'),
    re_path(r'^.*$', views.error_404, name='error_404'),
]

handler404 = 'tinyUrl.views.error_404'
