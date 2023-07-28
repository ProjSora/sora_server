from django.urls import re_path as url
from . import views

urlpatterns = [
    url('regist_user', views.RegistUser.as_view(), name='regist_user'),
    url('app_login', views.AppLogin.as_view(), name='app_login'),
    url('write_post', views.WritePost.as_view(), name='write_post'),
    url('read_post', views.ReadPost.as_view(), name='read_post'),
    url('update_post', views.UpdatePost.as_view(), name='update_post'),
    url('delete_post', views.DeletePost.as_view(), name='delete_post'),
]