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
        if check_password(user_pw, user.user_pw) is True:
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
    
class ReadUserInfo(APIView):
    '''
        사용자 정보 조회 시 사용되는 API
        - request.data에 user_id를 담아서 POST 요청을 보내면 아래 사항 확인
        - 해당 user_id의 사용자가 존재하면
        - UserInfo data return
        - 해당 user_id의 사용자가 존재하지 않으면
        - msg: "해당 사용자가 존재하지 않습니다."를 반환
    '''
    def post(self, request):
        user_id = request.data.get('user_id', "")
        user = UserInfo.objects.filter(user_id=user_id).first()
        
        if user is None:
            return Response(dict(msg="해당 사용자가 존재하지 않습니다."))
        
        return Response(data=UserSerializer(user).data)
    
    
class UpdateUserInfo(APIView):
    '''
        사용자 정보 수정 시 사용되는 API
        - request.data에 user_id를 담아서 POST 요청을 보내면 아래 사항 확인
        - 해당 user_id의 사용자가 존재하면
        - msg: "사용자 정보 수정에 성공했습니다.",
        - 수정 된 사용자 정보를 반환
        - 해당 user_id의 사용자가 존재하지 않으면
        - msg: "해당 사용자가 존재하지 않습니다."를 반환
    '''
    def post(self, request):
        user_id = request.data.get('user_id', "")
        user = UserInfo.objects.filter(user_id=user_id).first()
        
        if user is None:
            return Response(dict(msg="해당 사용자가 존재하지 않습니다."))
        
        for item in request.data:
            if item == "user_pw":
                user.user_pw = make_password(request.data[item])
            elif item == "phone_number":
                user.phone_number = request.data[item]
            elif item == "university":
                user.university = request.data[item]
                user.auth = False
                user.student_id = ""
                user.department = ""
            elif item == "student_id":
                user.student_id = request.data[item]
                user.department = ""
                user.auth = False
            elif item == "department":
                user.department = request.data[item]
                user.auth = False
            elif item == "description":
                user.description = request.data[item]
                
        
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=UserSerializer(user).data)
        return Response(serializer.errors)
    
class DeleteUserInfo(APIView):
    '''
        사용자 정보 삭제 시 사용되는 API
        - request.data에 user_id를 담아서 POST 요청을 보내면 아래 사항 확인
        - 해당 user_id의 사용자가 존재하면
        - msg: "사용자 정보 삭제에 성공했습니다."를 반환
        - 해당 user_id의 사용자가 존재하지 않으면
        - msg: "해당 사용자가 존재하지 않습니다."를 반환
    '''
    def post(self, request):
        user_id = request.data.get('user_id', "")
        user = UserInfo.objects.filter(user_id=user_id).first()
        
        if user is None:
            return Response(dict(msg="해당 사용자가 존재하지 않습니다."))
        
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.delete()
            return Response(dict(msg="사용자 정보 삭제에 성공했습니다."))
        
class WritePost(APIView):
    '''
        게시글 작성 시 사용되는 API
        - request.data에 user_id, post_name, post_content를 담아서 POST 요청을 보내면 아래 사항 확인
        - 게시글 제목이 없으면,
        - msg: "게시글 제목을 입력해주세요."를 반환
        - 게시글 내용이 없으면,
        - msg: "게시글 내용을 입력해주세요."를 반환
        - 작성 권한이 없으면,
        - msg: "작성 권한이 없습니다."를 반환
        - 게시글 작성에 성공하면,
        - msg: "게시글 작성에 성공했습니다."를 반환
    '''
    def post(self, request):
        user_id = request.data.get('user_id', "")
        post_title = request.data.get('post_title', "")
        post_content = request.data.get('post_content', "")
        user = UserInfo.objects.get(user_id=user_id)
        
        if post_title == "":
            return Response(dict(msg="게시글 제목을 입력해주세요."))
        if post_content == "":
            return Response(dict(msg="게시글 내용을 입력해주세요."))
        if user.auth == False:
            return Response(dict(msg="작성 권한이 없습니다."))
        
        post = Post.objects.create(user_id=user, post_title=post_title, post_content=post_content)
        #return Response(dict(msg="게시글 작성에 성공했습니다."))
        return Response(dict(msg="게시글 작성에 성공했습니다.", 
                            post_id=post.post_id, post_title=post.post_title, 
                            post_content=post.post_content, create_at=post.create_at, 
                            update_at=post.update_at))

class ReadPost(APIView):
    '''
        게시글 조회시 사용하는 API
        - request.data에 post_id를 담아서 POST 요청을 보내면 아래 사항 확인
        - 해당 post_id의 게시글이 존재하지 않으면,
        - msg: "해당 게시글이 존재하지 않습니다."를 반환
        - 해당 post_id의 게시글이 존재하면,
        - msg: "게시글 조회에 성공했습니다.",
        - post_views + 1, post_id, post_title, post_content을 반환
    '''
    def post(self, request):
        post_id = request.data.get('post_id', "")
        post = Post.objects.filter(post_id=post_id).first()
        
        if post is None:
            return Response(dict(msg="해당 게시글이 존재하지 않습니다."))
        
        post.post_views += 1
        post.save()
        return Response(dict(msg="게시글 조회에 성공했습니다.", 
                            post_id=post.post_id, post_views=post.post_views,
                            post_title=post.post_title, 
                            post_content=post.post_content))
        
class UpdatePost(APIView):
    '''
        게시글 수정시 사용하는 API
        - request.data에 post_id, post_title, post_content를 담아서 POST 요청을 보내면 아래 사항 확인
        - 해당 post_id의 게시글이 존재하지 않으면,
        - msg: "해당 게시글이 존재하지 않습니다."를 반환
        - 해당 post_id의 게시글이 존재하면,
        - msg: "게시글 수정에 성공했습니다.",
        - post_title, post_content, update_at을 반환
        - post_title이 없으면,
        - msg: "게시글 제목을 입력해주세요."를 반환
        - post_content가 없으면,
        - msg: "게시글 내용을 입력해주세요."를 반환
        - update_at 수정
    '''
    def post(self, request):
        post_id = request.data.get('post_id', "")
        post_title = request.data.get('post_title', "")
        post_content = request.data.get('post_content', "")
        post = Post.objects.filter(post_id=post_id).first()
        
        if post is None:
            return Response(dict(msg="해당 게시글이 존재하지 않습니다."))
        
        if post_title == "":
            return Response(dict(msg="게시글 제목을 입력해주세요."))
        if post_content == "":
            return Response(dict(msg="게시글 내용을 입력해주세요."))
        
        post.post_title = post_title
        post.post_content = post_content
        post.save()
        return Response(dict(msg="게시글 수정에 성공했습니다."))

class DeletePost(APIView):
    '''
        게시글 삭제시 사용하는 API
        - request.data에 post_id를 담아서 POST 요청을 보내면 아래 사항 확인
        - 해당 post_id의 게시글이 존재하지 않으면,
        - msg: "해당 게시글이 존재하지 않습니다."를 반환
        - 해당 post_id의 게시글이 존재하면,
        - msg: "게시글 삭제에 성공했습니다."를 반환
    '''
    def post(self, request):
        post_id = request.data.get('post_id', "")
        post = Post.objects.filter(post_id=post_id).first()
        
        if post is None:
            return Response(dict(msg="해당 게시글이 존재하지 않습니다."))
        
        post.delete()
        return Response(dict(msg="게시글 삭제에 성공했습니다."))