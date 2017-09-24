from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.Login, name='login'),
    url(r'^logout/$', views.Logout, name='logout'),
    url(r'^watched/$', views.Watched, name='watched'),
    url(r'^signup/$', views.Signup, name='signup'),
    url(r'^unwatched/$', views.Unwatched, name='unwatched'),
    url(r'^watched/(?P<movieid>\d+)/$', views.AddToWatched, name='watchedMovie'),
]
