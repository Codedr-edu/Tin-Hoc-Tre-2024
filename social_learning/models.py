from django.db import models
from django.contrib.auth.models import User


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
    address = models.TextField()
    address_password = models.TextField()
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
