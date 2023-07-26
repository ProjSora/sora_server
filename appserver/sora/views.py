from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from .serializer import UserSerializer

class AppLogin(APIView):
    def post(self, request):
        email = request.data.get('email', "")
        user_pw = request.data.get('user_pw', "")
        user = UserInfo.objects.filter(email=email).first()
        
        if user is None:
            return Response(dict(msg="해당 email의 사용자가 없습니다."))
        if check_password(user_pw, user.user_pw) is False:
            return Response(dict(msg="로그인 성공", user_id=user.user_id, university=user.university,
                                student_id=user.student_id, department=user.department, description=user.description))
        else:
            return Response(dict(msg="비밀번호가 일치하지 않습니다."))
        
class RegistUser(APIView):
    def post(self, request):
        serializer = UserSerializer(request.data)
        
        if UserInfo.objects.filter(email=serializer.data["email"]).exists():
            user = UserInfo.objects.filter(email=serializer.data["email"]).first()
            data = dict(
                msg="이미 가입 된 이메일입니다.",
                user_id=user.user_id,
                user_pw=user.user_pw,
            )
            return Response(data)
        
        if UserInfo.objects.filter(phone_number=serializer.data["phone_number"]).exists():
            user = UserInfo.objects.filter(phone_number=serializer.data["phone_number"]).first()
            data = dict(
                msg="이미 가입 된 전화번호입니다.",
                user_id=user.user_id,
                user_pw=user.user_pw,
            )
            return Response(data)
        
        user = serializer.create(serializer.data)
        
        return Response(data=UserSerializer(user).data)