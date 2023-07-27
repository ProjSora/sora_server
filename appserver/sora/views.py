from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from .serializer import UserSerializer

class AppLogin(APIView):
    '''
        어플리케이션 로그인 시 사용되는 API
        - request.data에 email, user_pw를 담아서 POST 요청을 보내면 아래 사항 확인
        - 해당 email의 사용자가 존재하고, 비밀번호가 일치하면
        - msg: "로그인 성공", user_id, university, student_id, department, description을 반환
        - 해당 email의 사용자가 존재하지 않으면
        - msg: "해당 email의 사용자가 없습니다."를 반환
        - 비밀번호가 일치하지 않으면
        - msg: "비밀번호가 일치하지 않습니다."를 반환
    '''
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
    '''
        회원가입 시 사용되는 API
        - request.data에 email, user_pw, university, student_id, department, description을 담아서 POST 요청을 보내면 아래 사항 확인
        - 해당 email의 사용자가 존재하면
        - msg: "이미 가입 된 이메일입니다.", user_id, user_pw를 반환
        - 해당 전화번호의 사용자가 존재하면
        - msg: "이미 가입 된 전화번호입니다.", user_id, user_pw를 반환
        - 해당 email, 전화번호의 사용자가 존재하지 않으면
        - msg: "회원가입 성공", user_id, user_pw를 반환
        - user_id는 자동으로 생성되며, user_pw는 암호화되어 저장됨
    '''
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