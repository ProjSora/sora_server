from django.contrib import admin
from .models import *

# Register your models here.
for model in [UserInfo, Message, ChatRoom, ChatRoomUser, Follower]:
    admin.site.register(model)