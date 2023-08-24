from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    def create(self, valiated_date):
        valiated_date['user_pw'] = make_password(valiated_date['user_pw'])
        user = UserInfo.objects.create(**valiated_date)
        return user
    
    def validate(self, attrs):
        return attrs
    
    class Meta:
        model = UserInfo
        fields = ("user_id", "email", "user_pw", "gender", "phone_number",
                "university", "student_id", "department", "description",  "user_name", "user_nick", "user_mbti",
                "create_at", "update_at", "auth")