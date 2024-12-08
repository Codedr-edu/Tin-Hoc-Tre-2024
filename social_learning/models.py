from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator


class Education_rank(models.Model):
    name = models.CharField(max_length=100)


class Subject(models.Model):
    name = models.CharField(max_length=1000)


class Bio(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="bio_user")
    description = models.TextField()
    facebook = models.CharField(max_length=1000, null=True, blank=True)
    instagram = models.CharField(max_length=1000, null=True, blank=True)
    twitter = models.CharField(max_length=1000, null=True, blank=True)
    zalo = models.CharField(max_length=1000, null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    balance = models.FloatField()
    wallet_passcode = models.TextField()
    deleted = models.IntegerField()
    edu_rank = models.ForeignKey(
        Education_rank, on_delete=models.CASCADE, related_name="user_edu_rank")
    avatar = models.ImageField(upload_to="images/", null=True, blank=True)
    thumbnail = models.ImageField(upload_to="images/", null=True, blank=True)


class Question(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="question_user")
    file = models.FileField(upload_to="files/questions/")
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="subject")
    education_rank = models.ForeignKey(
        Education_rank, on_delete=models.CASCADE, related_name="Education_rank_question")
    grade = models.IntegerField()
    price = models.FloatField()
    answered = models.IntegerField()
    like = models.ManyToManyField(
        Bio, related_name="question_like")
    dislike = models.ManyToManyField(
        Bio, related_name="question_dislike")
    status = models.CharField(max_length=1000)
    down = models.ManyToManyField(
        Bio, related_name="question_down")
    datetime = models.DateTimeField(auto_now_add=True)
    comment_counter = models.IntegerField()


class Answer(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    file = models.FileField(upload_to="files/answers/")
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="ques_select")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="question_user_answer")
    like = models.ManyToManyField(
        Bio, related_name="answer_like")
    dislike = models.ManyToManyField(
        Bio, related_name="answer_dislike")
    down = models.ManyToManyField(
        Bio, related_name="answer_down")
    choosen = models.IntegerField()
    status = models.CharField(max_length=1000)
    datetime = models.DateTimeField(auto_now_add=True)


class Document(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    grade = models.IntegerField()
    price = models.FloatField()
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="Document_auth")
    edu_rank = models.ForeignKey(
        Education_rank, on_delete=models.CASCADE, related_name="doc_edu_rank")
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="document_subject")
    file = models.FileField(upload_to="files/documents/")
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    like = models.ManyToManyField(
        Bio, related_name="document_like")
    dislike = models.ManyToManyField(
        Bio,  related_name="document_dislike")
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1000)
    down = models.ManyToManyField(
        Bio, related_name="document_down")
    comment_counter = models.IntegerField()


class have_buy_document(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="document_check")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="Document_buyer")


class Comment_Document(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        Bio, related_name='comment_document_user', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Document, related_name='cmt_document', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=1000)
    down = models.ManyToManyField(
        Bio, related_name="comment_document_down")


class Post(models.Model):
    content = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    like = models.ManyToManyField(
        Bio, related_name="post_like_related")
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="post_auth_related")
    dislike = models.ManyToManyField(
        Bio, related_name="post_dislike_related")
    status = models.CharField(max_length=1000)
    down = models.ManyToManyField(
        Bio, related_name="post_down")
    datetime = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="post_subject")
    comment_counter = models.IntegerField()


class Comment_Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        Bio, related_name='comment_post_user_related', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Post, related_name='comment_post_related', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=1000)
    down = models.ManyToManyField(
        Bio, related_name="comment_post_down")


class bad_keyword(models.Model):
    keyword = models.TextField()
    status = models.TextField()


class hornorable(models.Model):
    goal = models.IntegerField()
    content = models.TextField()
    user = models.ForeignKey(
        Bio, related_name='honorable_related', on_delete=models.CASCADE, null=True)
    status = models.TextField()


class Quiz(models.Model):
    name = models.TextField()
    description = models.TextField()
    edu_rank = models.ForeignKey(
        Education_rank, on_delete=models.CASCADE, related_name="quiz_edu_rank")
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="quiz_subject")
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    grade = models.IntegerField()
    user = models.ForeignKey(
        Bio, on_delete=models.CASCADE, related_name="user_auth")
    number_of_question = models.IntegerField()


class Quiz_questions(models.Model):
    number = models.IntegerField()
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="question_quiz")
    name = models.TextField()
    a = models.TextField()
    b = models.TextField()
    c = models.TextField()
    d = models.TextField()
    correct = models.TextField()


class GPTeen_doc(models.Model):
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    doc = models.FileField(upload_to="files/gpteen/")


class GPTeen_University_doc(models.Model):
    doc = models.FileField(upload_to="files/university/")


class club(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    video = models.FileField(upload_to="club/video/")
    user = models.ForeignKey(
        Bio, models.CASCADE, related_name="club_creator_related")
    time = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(
        Subject, models.CASCADE, related_name="club_subject_related")
    like = models.ManyToManyField(
        Bio, related_name="club_like")
    dislike = models.ManyToManyField(
        Bio, related_name="club_dislike")
    status = models.CharField(max_length=1000)
    down = models.ManyToManyField(
        Bio, related_name="club_down")
    skill = models.TextField()


class club_role(models.Model):
    club = models.ForeignKey(club, models.CASCADE,
                             related_name="club_role")
    role = models.CharField(max_length=1000)


class club_member(models.Model):
    club = models.ForeignKey(club, models.CASCADE,
                             related_name="club_member_related")
    user = models.ForeignKey(
        Bio, models.CASCADE, related_name="club_member_account")
    role = models.ForeignKey(club_role, models.CASCADE,
                             related_name="club_member_role_related")
    description = models.TextField()
    contact = models.TextField()
    status = models.CharField(max_length=1000)


class club_image(models.Model):
    club = models.ForeignKey(club, models.CASCADE,
                             related_name="club_image_related")
    image = models.ImageField(upload_to="club/image/")


class club_comment(models.Model):
    content = models.TextField()
    club = models.ForeignKey(club, models.CASCADE,
                             related_name="club_comment_related")
    status = models.CharField(max_length=1000)
    user = models.ForeignKey(
        Bio, models.CASCADE, related_name="user_club_comment_related")
    down = models.ManyToManyField(
        Bio, related_name="club_comment_down")


class online_class(models.Model):
    user = models.ForeignKey(
        Bio, models.CASCADE, related_name="teacher_related")
    title = models.TextField()
    description = models.TextField()
    subject = models.ForeignKey(
        Subject, models.CASCADE, related_name="subject_online_class_related")
    edu_rank = models.ForeignKey(
        Education_rank, models.CASCADE, name="online_class_edu_rank")
    grade = models.IntegerField()
    platform = models.TextField()
    link = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to="online_class/image")
    like = models.ManyToManyField(
        Bio, related_name="online_class_like")
    dislike = models.ManyToManyField(
        Bio, related_name="online_class_dislike")
    status = models.CharField(max_length=1000)
    down = models.ManyToManyField(
        Bio, related_name="online_class_down")
    time = models.DateTimeField(auto_now_add=True)


class homework_online_class(models.Model):
    online_class = models.ForeignKey(
        online_class, models.CASCADE, related_name="online_class_homework")
    title = models.TextField()
    content = models.TextField()
    file = models.FileField(upload_to="online_class/homework/")
    # deadline = models.TextField()


class online_class_comment(models.Model):
    online_class = models.ForeignKey(
        online_class, models.CASCADE, related_name="online_class_comment_related")
    content = models.TextField()
    status = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    down = models.ManyToManyField(
        Bio, related_name="online_class_comment_down")
    user = models.ForeignKey(
        Bio, models.CASCADE, related_name="online_class_comment_user_related")


class online_class_buyer(models.Model):
    online_class = models.ForeignKey(
        online_class, models.CASCADE, related_name="online_class_buyer")
    user = models.ForeignKey(
        Bio, models.CASCADE, related_name="online_class_buyer_user")


class online_class_homework_submit(models.Model):
    homework = models.ForeignKey(
        homework_online_class, models.CASCADE, related_name="online_class_homework_related")
    user = models.ForeignKey(
        Bio, models.CASCADE, related_name="online_class_homework_submit_user_related")
    file = models.FileField(upload_to="online_class/homework/done/")
    teacher_review = models.TextField()
