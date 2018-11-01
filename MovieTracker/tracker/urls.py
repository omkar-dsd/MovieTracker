from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.gotoLogin, name='landing'),
    url(r'^login/$', views.Login, name='login'),
    url(r'^watched/$', views.WatchedView.as_view(), name='watched'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^signup/$', views.Signup, name='signup'),
    url(r'^unwatched/$', views.Unwatched, name='unwatched'),
    url(r'^watched/(?P<movieid>\d+)/$', views.AddToWatched, name='watchedMovie'),
    url(r'^description/(?P<movieid>\d+)/$', views.MovieDescription, name='movieDescription'),

]
