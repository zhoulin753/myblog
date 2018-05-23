# from django.contrib.auth.views import login,logout
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^enter/$', enter),
    url(r'^img/$', img),
    url(r'^enroll/$', enroll),
    url(r'^enroll_validate/$', enroll_validate),
    url(r'^blog/(\w*)$', blog),
    url(r'^(\w*)/article/(\d+)$', article_num),
    url(r'^logout/$', log_out),
    url(r'^up_down/$', up_down),
    url(r'^comment/$', comment),
    url(r'^write/$', write),
    url(r'^category$', category),
]
