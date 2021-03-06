from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^unpublished/$', views.post_unpublished_list, name='post_unpublished_list'),
    url(r'^post/(?P<pk>[0-9]+)/publisher/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<post_pk>[0-9]+)/comment_new/(?P<comment_pk>[0-9]+)/$', views.comment_new, name='comment_new'),
    url(r'^post/(?P<post_pk>[0-9]+)/comment_delete/(?P<comment_pk>[0-9]+)/$', views.comment_delete, name='comment_delete'),
]
