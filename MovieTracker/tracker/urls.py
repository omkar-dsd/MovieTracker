from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.Login),
    url(r'^logout/$', views.Logout),
    url(r'^watched/$', views.Watched),
    url(r'^signup/$', views.Signup),
    url(r'^unwatched/$', views.Unwatched),
]