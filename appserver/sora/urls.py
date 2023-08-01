from django.urls import re_path as url
from . import views

urlpatterns = [
    url('app_login', views.AppLogin.as_view(), name='app_login'),
    url('regist_user', views.RegistUser.as_view(), name='regist_user'),
    url('read_user', views.ReadUserInfo.as_view(), name='read_user'),
    url('update_user', views.UpdateUserInfo.as_view(), name='update_user'),
    url('delete_user', views.DeleteUserInfo.as_view(), name='delete_user'),
    url('write_post', views.WritePost.as_view(), name='write_post'),
    url('read_post', views.ReadPost.as_view(), name='read_post'),
    url('update_post', views.UpdatePost.as_view(), name='update_post'),
    url('delete_post', views.DeletePost.as_view(), name='delete_post'),
]