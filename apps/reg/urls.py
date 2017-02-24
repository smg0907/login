from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^travels/add$', views.addPlan),
    url(r'^logout$', views.logout)
    # url(r'^success/(?P<id>\d+)$', views.success),
]
