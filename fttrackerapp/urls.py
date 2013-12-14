from django.conf.urls import patterns, url
from fttrackerapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    url(r'^pollfortrucks/$', views.pollfortrucks, name='get latest truck locations'),
)