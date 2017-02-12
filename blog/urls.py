from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/addlike/(?P<post_id>\d+)/$', views.addlike),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^users/list/$', views.user_list, name='user_list'),
    url(r'^users/(?P<user_id>\d+)/$', views.user_detail, name='user_detail'),
    url(r'^profile_edit/(?P<profile_id>[0-9]+)?/$', views.edit_user, name="edit_profile"),
    url(r'^page/(\d+)/$', 'blog.views.post_list'),
]
