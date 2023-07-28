from django.db import models

class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name='이메일', max_length=255, null=False, default="")
    user_pw = models.CharField(max_length=255, null=False, default=False)
    gender = models.CharField(verbose_name='성별', max_length=10, null=False, default='male')
    phone_number = models.CharField(verbose_name='전화번호', max_length=11, null=False, default="")
    university = models.CharField(verbose_name='학교', max_length=20, null=False, default="")
    student_id = models.CharField(verbose_name='학번', max_length=20, null=False, default="")
    department = models.CharField(verbose_name='학과', max_length=20, null=False, default="")
    description = models.CharField(verbose_name='자기소개', max_length=255, null=False, default="")
    
    create_at = models.DateTimeField(verbose_name='생성일', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='수정일', auto_now=True)
    auth = models.BooleanField(verbose_name='인증여부', null=False, default=False)
    
    class Meta:
        db_table = 'user'
        verbose_name = '유저'
        
class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    message_content = models.CharField(verbose_name='메세지 내용', max_length=255, null=False, default="")
    create_at = models.DateTimeField(verbose_name='생성일', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='수정일', auto_now=True)
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, db_column='user_id', null=False)
    chat_id = models.ForeignKey('ChatRoom', on_delete=models.CASCADE, db_column='chat_id', null=False)

    class Meta:
        db_table = 'message'
        verbose_name = '메세지'

class ChatRoom(models.Model):
    chat_id = models.AutoField(primary_key=True)
    chat_name = models.CharField(verbose_name='채팅방 이름', max_length=255, null=False, default="")
    create_at = models.DateTimeField(verbose_name='생성일', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='수정일', auto_now=True)

    class Meta:
        db_table = 'chatroom'
        verbose_name = '채팅방'
        
class ChatRoomUser(models.Model):
    chat_id = models.ForeignKey('ChatRoom', on_delete=models.CASCADE, db_column='chat_id', null=False)
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, db_column='user_id', null=False)

    class Meta:
        db_table = 'chat_user'
        verbose_name = '채팅방 유저'
        
class Follower(models.Model):
    '''
        수정 필요
    '''
    follower_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, db_column='user_id', null=False)
    follow_accept = models.BooleanField(verbose_name='팔로우 수락 여부', default=False)
    
    class Meta:
        db_table = 'follower'
        verbose_name = '팔로워'
    
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, db_column='user_id', null=False)
    university = models.CharField(verbose_name='학교', max_length=20, null=False, default="")
    post_title = models.CharField(verbose_name='게시글 제목', max_length=255, null=False, default="")
    post_content = models.CharField(verbose_name='게시글 내용', max_length=255, null=False, default="")
    post_views = models.IntegerField(verbose_name='게시글 조회수', null=False, default=0)
    post_likes = models.IntegerField(verbose_name='게시글 좋아요 수', null=False, default=0)
    create_at = models.DateTimeField(verbose_name='생성일', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='수정일', auto_now=True)
    
    class Meta:
        db_table = 'post'
        verbose_name = '게시글'
        
class PostLikes(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, db_column='post_id', null=False)
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, db_column='user_id', null=False)
    
    class Meta:
        db_table = 'post_likes'
        verbose_name = '게시글 좋아요'