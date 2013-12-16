from django.conf.urls import patterns, url
from fttrackerapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    url(r'^pollfortrucks/$', views.poll_for_trucks, name='get latest truck locations'),
    url(r'^trucksatlocation/$', views.trucks_at_location, name='trucks currently at location'),
)
