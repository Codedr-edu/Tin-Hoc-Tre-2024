"""
Còn nhiều function chx đc add vào. Khi nào team hội ý và thống nhất đc thì add vào sau.
"""

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from .hashed import hashed
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.apps import AppConfig
import random
from django.db.models import Q
import datetime
import json
import hashlib
import os
from .GPTsearch import GPTeen
from .GPTsecurity import check_document, check_image, check_content
from .GPTeacher import search_document, search_image
import random
from .GPTformatter import check_and_format_content
from .GPTeen_university import gptu_check


'''
web3 = Web3(Web3.HTTPProvider(
    'https://sepolia.infura.io/v3/8c4c9235b7ed489ab0bc8c26795ae24e'))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"tokens","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeSub","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeDiv","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeMul","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeAdd","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"tokenOwner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Approval","type":"event"}]')
contract = web3.eth.contract(
    address='0x2519019C7251545be7B81521951874B2c4948A56', abi=abi)
'''
# authenticated


def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("check")
        else:
            return redirect("index")


def Signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        grade = request.POST.get("grade")
        education_rank = request.POST.get("edu_rank")
        description = request.POST.get("description")
        avatar = request.FILES['avatar']
        thumbnail = request.FILES['thumbnail']
        passcode = request.POST.get("passcode")

        user = User.objects.filter(username=username).first()
        user2 = Bio.objects.filter(user=user).first()

        if not user and not user2:
            user = User.objects.create_user(username, email, password)
            user.save()
            user = User.objects.filter(username=username).first()
            edu = Education_rank.objects.filter(id=education_rank).first()
            if user and edu:
                # key = create_private_key()
                passcode = hashed(passcode)
                bio = Bio(user=user, avatar=avatar, thumbnail=thumbnail, grade=grade, edu_rank=edu, deleted=0,
                          description=description, balance=1000, wallet_passcode=passcode)
                bio.save()
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                return redirect("check")
        else:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("check")


def check(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        if bio:
            return redirect('post')
        else:
            edu = Education_rank.objects.all()
            context = {"educations": edu}
            if request.method == "POST":
                grade = request.POST.get("grade")
                education_rank = request.POST.get("edu_rank")
                description = request.POST.get("description")
                avatar = request.FILES['avatar']
                thumbnail = request.FILES['thumbnail']
                passcode = request.POST.get("passcode")

                edu = Education_rank.objects.get(id=education_rank)

                # key = create_private_key()
                # wallet = create_account(key)

                passcode = hashed(passcode)
                bio = Bio(user=request.user, avatar=avatar, thumbnail=thumbnail, grade=grade, edu_rank=edu, deleted=0,
                          description=description, balance=1000, wallet_passcode=passcode)
                bio.save()
                return redirect('post')
    else:
        return redirect('index')
    return render(request, 'check.html', context)

# index


def index(request):
    if request.user.is_authenticated:
        return redirect('check')
    else:
        edu = Education_rank.objects.all()
        context = {"educations": edu}
    return render(request, "index.html", context)


# list_view


def question_list_view(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()

        edu_rank = Education_rank.objects.all()
        subject = Subject.objects.all()

        if request.method == "GET":
            search = request.GET.get("search")
            sub = request.GET.get("topic")

            if not search and not sub:
                post = Question.objects.filter(
                    grade__lte=bio.grade, education_rank=bio.edu_rank, status="Công khai").all()
            elif search and sub:
                sub = Subject.objects.filter(id=sub).first()
                post = Question.objects.filter(
                    Q(content__icontains=search), Q(title__icontains=search), grade__lte=bio.grade, subject=sub, education_rank=bio.edu_rank, status="Công khai").all()
            elif search and not sub:
                post = Question.objects.filter(
                    Q(content__icontains=search), Q(title__icontains=search), grade__lte=bio.grade, education_rank=bio.edu_rank, status="Công khai").all()
            else:
                sub = Subject.objects.filter(id=sub).first()
                post = Question.objects.filter(
                    grade__lte=bio.grade, subject=sub, education_rank=bio.edu_rank, status="Công khai").all()
        else:
            post = Question.objects.filter(
                grade__lte=bio.grade, education_rank=bio.edu_rank, status="Công khai").all()

        context = {"posts": post[::-1], "bio": bio,
                   'subjects': subject, 'educations': edu_rank}
    else:
        return redirect("index")
    return render(request, "question/list.html", context)


def document_list_view(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()

        edu_rank = Education_rank.objects.all()
        subject = Subject.objects.all()

        if request.method == "GET":
            search = request.GET.get("search")
            sub = request.GET.get("topic")

            if not search and not sub:
                post = Document.objects.filter(
                    grade__lte=bio.grade, edu_rank=bio.edu_rank, status="Công khai").all()
            elif search and sub:
                sub = Subject.objects.filter(id=sub).first()
                post = Document.objects.filter(
                    Q(content__icontains=search), Q(title__icontains=search), grade__lte=bio.grade, subject=sub, edu_rank=bio.edu_rank, status="Công khai").all()
            elif search and not sub:
                post = Document.objects.filter(
                    Q(content__icontains=search), Q(title__icontains=search), grade__lte=bio.grade, edu_rank=bio.edu_rank, status="Công khai").all()
            else:
                sub = Subject.objects.filter(id=sub).first()
                post = Document.objects.filter(
                    grade__lte=bio.grade, subject=sub, edu_rank=bio.edu_rank, status="Công khai").all()
        else:
            post = Document.objects.filter(
                grade__lte=bio.grade, edu_rank=bio.edu_rank, status="Công khai").all()

        context = {"posts": post[::-1], "bio": bio,
                   'subjects': subject, 'educations': edu_rank}
    else:
        return redirect("index")
    return render(request, "document/list.html", context)


def post_list_view(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        subject = Subject.objects.all()
        cmt = Comment_Post.objects
        if request.method == "GET":
            search = request.GET.get("search")
            topic = request.GET.get("topic")
            if topic and not search:
                s2 = Subject.objects.filter(id=topic).first()
                post = Post.objects.filter(
                    subject=s2, status="Công khai").all()
            elif search and not topic:
                post = Post.objects.filter(
                    Q(content__icontains=search), status="Công khai").all()
            elif search and topic:
                s2 = Subject.objects.filter(id=topic).first()
                post = Post.objects.filter(
                    Q(content__icontains=search), subject=s2, status="Công khai").all()
            else:
                post = Post.objects.filter(status="Công khai").all()
        else:
            post = Post.objects.filter(subject=s2, status="Công khai").all()

        context = {"posts": post[::-1],
                   "subjects": subject, "bio": bio, "cmts": cmt}
    else:
        return redirect("index")
    return render(request, "post/list.html", context)


# create_api


def post_create(request):
    if request.user.is_authenticated:
        user = Bio.objects.filter(user=request.user).first()
        # bad = bad_keyword.objects.filter(status="Cấm").all()
        if request.method == "POST":
            content = request.POST.get("content")
            image = request.FILES.get("image")
            # video = request.FILE.get("video")
            subject = Subject.objects.filter(
                id=request.POST.get("subject")).first()

            sql = Post(content=content, user=user, subject=subject, image=image,
                       status="Chờ kiểm duyệt", comment_counter=0)
            sql.save()

            check_cnt = check_and_format_content(content)
            if sql.image:
                check_img = check_image(image=sql.image.url)
            else:
                check_img = "Pass"
            fail = "có nội dung nhạy cảm"
            if check_cnt != fail or check_img != fail:
                sql.status = "Công khai"
                sql.content = check_cnt[8:-4]
                sql.save()

            return redirect("success", status=sql.status)
    else:
        return redirect("index")


def document_create(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            image = request.FILES.get("image")
            file = request.FILES.get('file')
            grade = request.POST.get("grade")
            price = request.POST.get("price")
            # video = request.FILE.get("video")
            edu_rank = request.POST.get("education_rank")
            subject = request.POST.get("subject")

            edu_rank = Education_rank.objects.get(id=edu_rank)
            subject = Subject.objects.get(id=subject)

            sql = Document(title=title, description=description, file=file, image=image, status="Chờ kiểm duyệt",
                           grade=grade, edu_rank=edu_rank, user=user, price=price, subject=subject, comment_counter=0)
            sql.save()
            # sql = Document.objects.filter()

            check_doc = check_document(image=sql.file.url)
            if sql.image:
                check_img = check_image(image=sql.image.url)
            else:
                check_img = "Pass"
            check_title = check_content(sql.title)
            check_description = check_and_format_content(sql.description)
            fail = "có nội dung nhạy cảm"
            if check_doc != fail and check_img != fail and check_title != fail and check_description != fail:
                sql.status = "Công khai"
                sql.description = check_description[8:-4]
                sql.save()

            return redirect("success", status=sql.status)
    else:
        return redirect("index")


def question_create(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            file = request.FILES.get("file")
            image = request.FILES.get("image")
            grade = request.POST.get("grade")
            # video = request.FILE.get("video")
            edu_rank = request.POST.get("education_rank")
            subject = request.POST.get("subject")
            price = int(request.POST.get("price"))

            edu_rank = Education_rank.objects.filter(id=edu_rank).first()
            subject = Subject.objects.filter(id=subject).first()

            sql = Question(title=title, description=description, price=price, file=file, status="Chờ kiểm duyệt",
                           subject=subject, image=image, grade=grade, education_rank=edu_rank, user=user, answered=0, comment_counter=0)
            sql.save()

            if sql.file:
                check_doc = check_document(image=sql.image.url)
            else:
                check_doc = "Pass"
            if sql.image:
                check_img = check_image(image=sql.image.url)
            else:
                check_img = "Pass"
            check_title = check_content(sql.title)
            check_description = check_and_format_content(sql.description)
            fail = "có nội dung nhạy cảm"
            if check_doc != fail and check_img != fail and check_title != fail and check_description != fail:
                sql.status = "Công khai"
                sql.description = check_description[8:-4]
                sql.save()

            return redirect("success", status=sql.status)
    else:
        return redirect("index")


# payment_api
def question_payment(request, id):
    if request.user.is_authenticated:
        answer = Answer.objects.filter(id=id).first()
        question = Question.objects.filter(id=answer.question.id).first()
        if request.method == "POST" and question:
            code = request.POST.get("code")

            final = hashed(code)
            if final != "ValueError: The passcode just contain only number from 0 to 9":
                bio = Bio.objects.filter(
                    wallet_passcode=final, user=request.user).first()
                honor_set = hornorable.objects.filter(user=answer.user).count()
                if final == bio.wallet_passcode and bio.balance >= question.price and question.answered != 1:
                    answer.user.balance += question.price
                    bio.balance -= question.price
                    answer.user.save()
                    bio.save()
                    if answer.user.balance >= 10**(honor_set+1):
                        content = "Bạn", answer.user.user.username, "đã đạt mức điểm", 10**(
                            honor_set+1)
                        honor = hornorable(
                            goal=10**(honor_set+1), content=content, user=answer.user, status="Chờ xử lý")
                        honor.save()
                    return redirect("question_bill", id=id)
                else:
                    return redirect("all_error")
            else:
                return redirect("all_error")
    else:
        return redirect("index")


def document_payment(request, id):
    if request.user.is_authenticated:
        document = Document.objects.filter(id=id).first()
        if request.method == "POST":
            code = request.POST.get("code")

            final = hashed(code)
            if final != "ValueError: The passcode just contain only number from 0 to 9":
                bio = Bio.objects.filter(
                    wallet_passcode=final, user=request.user).first()
                honor_set = hornorable.objects.filter(
                    user=document.user).count()
                if final == bio.wallet_passcode and bio.balance >= document.price:
                    document.user.balance += document.price
                    bio.balance -= document.price
                    document.user.save()
                    bio.save()
                    sql = have_buy_document(document=document, user=bio)
                    sql.save()
                    if answer.user.balance >= 10**(honor_set+1):
                        content = "Bạn", document.user.user.username, "đã đạt mức điểm", 10**(
                            honor_set+1)
                        honor = hornorable(
                            goal=10**(honor_set+1), content=content, user=document.user, status="Chờ xử lý")
                        honor.save()
                    return redirect("document_bill", id=id)
                else:
                    return redirect("all_error")
            else:
                return redirect("all_error")
    else:
        return redirect("index")


def post_payment(request, id):
    if request.user.is_authenticated:
        document = Post.objects.filter(id=id).first()
        if request.method == "POST":
            value = float(request.POST.get("value"))
            code = request.POST.get("code")

            final = hashed(code)
            if final != "ValueError: The passcode just contain only number from 0 to 9":
                bio = Bio.objects.filter(
                    wallet_passcode=final, user=request.user).first()
                honor_set = hornorable.objects.filter(
                    user=document.user).count()
                if final == bio.wallet_passcode and bio.balance >= value:
                    document.user.balance += value
                    bio.balance -= value
                    document.user.save()
                    bio.save()
                    if answer.user.balance >= 10**(honor_set+1):
                        content = "Bạn", document.user.user.username, "đã đạt mức điểm", 10**(
                            honor_set+1)
                        honor = hornorable(
                            goal=10**(honor_set+1), content=content, user=document.user, status="Chờ xử lý")
                        honor.save()
                    goal = "/bill/post/"+str(id)+"/value/"+str(int(value))
                    return redirect(goal)
                else:
                    return redirect("all_error")
            else:
                return redirect("all_error")
    else:
        return redirect("index")
    return render(request, "post/code_submit.html")


'''

def question_payment(request, id):
    if request.user.is_authenticated:
        answer = Answer.objects.filter(id=id).first()
        question = Question.objects.filter(id=answer.question.id).first()

        if request.method == "POST" and question:
            code = request.POST.get("code")

            final = hashed(code)
            if final != "ValueError: The passcode just contain only number from 0 to 9":
                bio = Bio.objects.filter(
                    wallet_passcode=final, user=request.user).first()
                teen_balanced = float(web3.to_wei(
                    contract.functions.balanceOf(bio.address).call(), 'ether'))
                if final == bio.wallet_passcode and teen_balanced >= question.price and question.answered != 1:

                    os.environ["real_password_question" +
                               bio.user.username] = bio.address_password
                    real_password = os.getenv(
                        "real_password_document"+bio.user.username)

                    question.answered = 1
                    question.save()

                    answer.choosen = 1
                    answer.save()

                    tran = contract.functions.transfer(question.user.address, web3.to_wei(question.price, 'ether')).build_transaction(
                        {'chainId': 11155111, 'gas': 21632, 'nonce': web3.eth.get_transaction_count(bio.address), 'value': 0})
                    signed_txn = web3.eth.account.sign_transaction(
                        tran, real_password)
                    web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                    return redirect("question_bill", id=id)
                else:
                    return redirect("all_error")
            else:
                return redirect("index")
    return render(request, "question/code_submit.html")


def document_payment(request, id):
    if request.user.is_authenticated:
        document = Document.objects.filter(id=id).first()
        if request.method == "POST":
            code = request.POST.get("code")

            final = hashed(code)
            if final != "ValueError: The passcode just contain only number from 0 to 9":
                bio = Bio.objects.filter(
                    wallet_passcode=final, user=request.user).first()
                teen_balanced = float(web3.to_wei(
                    contract.functions.balanceOf(bio.address).call(), 'ether'))
                if final == bio.wallet_passcode and teen_balanced >= document.price:

                    os.environ["real_password_document" +
                               bio.user.username] = bio.address_password
                    real_password = os.getenv(
                        "real_password_document"+bio.user.username)

                    tran = contract.functions.transfer(str(document.user.address), web3.to_wei(int(document.price), 'ether')).build_transaction(
                        {'chainId': 11155111,
                         'gas': 2163200,
                         'nonce': web3.eth.get_transaction_count(bio.address), 'value': 0})
                    signed_txn = web3.eth.account.sign_transaction(
                        tran, real_password)
                    web3.eth.send_raw_transaction(signed_txn.rawTransaction)

                    sql = have_buy_document(document=document, user=bio)
                    sql.save()

                    return redirect("document_bill", id=id)
                else:
                    return redirect("all_error")
            else:
                return redirect("all_error")
    else:
        return redirect("index")


def post_payment(request, id):
    if request.user.is_authenticated:
        document = Post.objects.filter(id=id).first()
        if request.method == "POST":
            value = float(request.POST.get("value"))
            code = request.POST.get("code")

            final = hashed(code)
            if final != "ValueError: The passcode just contain only number from 0 to 9":
                bio = Bio.objects.filter(
                    wallet_passcode=final, user=request.user).first()
                teen_balanced = float(web3.to_wei(
                    contract.functions.balanceOf(bio.address).call(), 'ether'))
                if final == bio.wallet_passcode and teen_balanced >= value:

                    os.environ["real_password_document" +
                               bio.user.username] = bio.address_password
                    real_password = os.getenv(
                        "real_password_document"+bio.user.username)

                    tran = contract.functions.transfer(str(document.user.address), web3.to_wei(int(value), 'ether')).build_transaction(
                        {'chainId': 11155111,
                         'gas': 2163200,
                         'nonce': web3.eth.get_transaction_count(bio.address), 'value': 0})
                    signed_txn = web3.eth.account.sign_transaction(
                        tran, real_password)
                    web3.eth.send_raw_transaction(signed_txn.rawTransaction)

                    goal = "/bill/post/"+str(id)+"/value/"+str(int(value))
                    return redirect(goal)
                else:
                    return redirect("all_error")
            else:
                return redirect("all_error")
    else:
        return redirect("index")
    return render(request, "post/code_submit.html")


# transfer_api


def teen_transfer(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            post = Bio.objects.filter(id=request.POST.get("to_user")).first()
            code = request.POST.get("passcode")
            value = request.POST.get("value")
            if code and value:
                final = hashed(code)
                if final != "ValueError: The passcode just contain only number from 0 to 9":
                    bio = Bio.objects.filter(
                        wallet_passcode=final, user=request.user).first()
                    teen_balanced = float(web3.to_wei(
                        contract.functions.balanceOf(bio.address).call(), 'ether'))
                    eth_balanced = float(eth_balanced=float(
                        web3.to_wei(web3.eth.get_balance(post.address), 'ether')))
                    if teen_balanced >= post.changed_value and eth_balanced >= post.change_value:

                        os.environ["real_password_teen_transfer" +
                                   bio.user.username] = bio.address_password
                        real_password = os.getenv(
                            "real_password_teen_transfer"+bio.user.username)

                        tran = contract.functions.transfer(post.user.address, web3.to_wei(value, 'ether')).build_transaction(
                            {'chainId': 11155111, 'gas': 2163200, 'nonce': web3.eth.get_transaction_count(bio.address), 'value': 0})
                        signed_txn = web3.eth.account.sign_transaction(
                            tran, real_password)
                        web3.eth.send_raw_transaction(
                            signed_txn.rawTransaction)
                        return redirect("your_profile")
                    else:
                        return redirect("all_error")
                else:
                    return redirect("all_error")
            else:
                return redirect("index")


def eth_transfer(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            post = Bio.objects.filter(id=id).first()
            code = request.POST.get("passcode")
            value = request.POST.get("value")
            if code and value:
                final = hashed(code)
                if final != "ValueError: The passcode just contain only number from 0 to 9":
                    bio = Bio.objects.filter(
                        wallet_passcode=final, user=request.user).first()
                    teen_balanced = float(web3.to_wei(
                        contract.functions.balanceOf(bio.address).call(), 'ether'))
                    eth_balanced = float(eth_balanced=float(
                        web3.to_wei(web3.eth.get_balance(post.address), 'ether')))
                    if teen_balanced >= post.changed_value and eth_balanced >= post.change_value:
                        os.environ["real_password_eth" +
                                   post.user.username] = post.user.address_password
                        test2 = os.getenv(
                            "real_password_eth"+post.user.username)
                        tran = {'chainId': 11155111, 'gas': 2163200, 'nonce': web3.eth.get_transaction_count(
                            bio.address), 'to': post.address, 'value': web3.to_wei(value, 'ether')}
                        signed_txn = web3.eth.account.sign_transaction(
                            tran, test2)
                        web3.eth.send_raw_transaction(
                            signed_txn.rawTransaction)
                        return redirect("your_profile")
                    else:
                        return redirect("all_error")
                else:
                    return redirect("all_error")
            else:
                return redirect("index")


'''
# like_api


def like_post(request, id):
    if request.user.is_authenticated:
        post = Post.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if not bio in post.like.all():
            post.like.add(bio)
            goal = "/post/#"+str(id)
            return redirect(goal)
        else:
            post.like.remove(bio)
            goal = "/post/#"+str(id)
            return redirect(goal)
    else:
        return redirect("index")


def like_document(request, id):
    if request.user.is_authenticated:
        post = Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if not bio in post.like.all():
            post.like.add(bio)
            return redirect("document_view", id=id)
        else:
            post.like.remove(bio)
            return redirect("document_view", id=id)
    else:
        return redirect("index")


def like_question(request, id):
    if request.user.is_authenticated:
        post = Question.objects.get(id=id)
        bio = Bio.objects.get(user=request.user)
        if not bio in post.like.all():
            post.like.add(bio)
            return redirect("question_view", id=id)
        else:
            post.like.remove(bio)
            return redirect("question_view", id=id)
    else:
        return redirect("index")


def like_answer(request, id):
    if request.user.is_authenticated:
        post = Answer.objects.get(id=id)
        bio = Bio.objects.filter(user=request.user).first()
        if not bio in post.like.all():
            post.like.add(bio)
            return redirect("question_view", id=post.question.id)
        else:
            post.like.remove(bio)
            return redirect("question_view", id=post.question.id)
    else:
        return redirect("index")

# dislike_api


def dislike_post(request, id):
    if request.user.is_authenticated:
        post = Post.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.dislike.all():
            post.dislike.add(bio)
            goal = "/posts/#"+str(id)+"/"
            return redirect(goal)
        else:
            post.dislike.remove(bio)
            goal = "/posts/#"+str(id)+"/"
            return redirect(goal)
    else:
        return redirect("index")


def dislike_document(request, id):
    if request.user.is_authenticated:
        post = Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.dislike.all():
            post.dislike.add(bio)
            return redirect("document_view", id=id)
        else:
            post.dislike.remove(bio)
            return redirect("document_view", id=id)
    else:
        return redirect("index")


def dislike_question(request, id):
    if request.user.is_authenticated:
        post = Question.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.dislike.all():
            post.dislike.add(bio)
            return redirect("read_question", id=id)
        else:
            post.dislike.remove(bio)
            return redirect("read_question", id=id)
    else:
        return redirect("index")


def dislike_answer(request, id):
    if request.user.is_authenticated:
        post = Answer.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.dislike.all():
            post.dislike.add(bio)
            return redirect("read_question", id=post.question.id)
        else:
            post.dislike.remove(bio)
            return redirect("read_question", id=post.question.id)
    else:
        return redirect("index")

# comment_api


def comment_post_view(request, id):
    if request.user.is_authenticated:
        comments = Comment_Post.objects.filter(post__id=id).all()
        post = Post.objects.filter(id=id).first()
        context = {'comments': comments, 'post': post}
    else:
        return redirect("index")
    return render(request, "post/comment_view.html", context)


def comment_post(request, id):
    if request.user.is_authenticated:
        post = Post.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        # bad = bad_keyword.objects(status="Cấm").all()
        if post and bio:
            if request.method == "POST":
                content = request.POST.get("content")

                check = "Công khai"
                check_cnt = check_content(content)
                fail = "có nội dung nhạy cảm"
                if check_cnt == fail:
                    check = "Chờ kiểm duyệt"

                sql = Comment_Post(post=post, user=bio,
                                   content=content, status=check)
                sql.save()
                post.comment_counter += 1
                post.save()

                return redirect("success", status=check)
        else:
            return redirect("post_view", id=id)
    else:
        return redirect("index")


def comment_document(request, id):
    if request.user.is_authenticated:
        post = Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        # bad = bad_keyword.objects.filter(status="Cấm").all()
        if post and bio:
            if request.method == "POST":
                content = request.POST.get("content")

                check = "Công khai"
                check_cnt = check_content(content)
                fail = "có nội dung nhạy cảm"
                if check_cnt == fail:
                    check = "Chờ kiểm duyệt"

                status = check

                sql = Comment_Document(
                    post=post, user=bio, content=content, status=status)
                sql.save()
                return redirect("success", status=status)
        else:
            return redirect("document_view", id=id)
    else:
        return redirect("index")


def answer(request, id):
    if request.user.is_authenticated:
        post = Question.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method == "POST":
                content = request.POST.get("content")
                file = request.FILES.get("file")
                image = request.FILES.get("image")

                sql = Answer(question=post, user=bio, status="Chờ kiểm duyệt",
                             content=content, image=image, file=file, choosen=0)
                sql.save()

                check_cnt = check_content(content)
                check_img = check_image(sql.image.url)
                check_doc = check_document(sql.file.url)
                fail = "có nội dung nhạy cảm"
                if check_cnt != fail and check_img != fail and check_doc != fail:
                    sql.status = "Công khai"
                    sql.save()

                return redirect("success", status=sql.status)
        else:
            return redirect("read_question", id=id)
    else:
        return redirect("index")

# reply_comment_api


def reply_comment_post(request, id):
    if request.user.is_authenticated:
        post = Comment_Post.objects.filter(id=id).first()
        p = Post.objects.filter(id=post.post.id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method == "POST":
                content = request.POST.get("content")

                sql = Comment_Post(post=post.post, user=bio,
                                   content=content, reply=post)
                sql.save()

                return redirect("success")
        else:
            return redirect("read_post", id=id)
    else:
        return redirect("index")


def reply_comment_document(request, id):
    if request.user.is_authenticated:
        post = Comment_Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method == "POST":
                content = request.POST.get("content")

                sql = Comment_Document(
                    post=post.post, user=bio, content=content, reply=post)
                sql.save()

                post.comment_counter += 1
                post.save()

                sql = Comment_Document.objects.filter(
                    post=post.post, user=bio, content=content, reply=post).first()
                goal = "/document/"+str(id)+"/#"+str(sql.id)+"/"
                return redirect(goal)
        else:
            return redirect("read_gig", id=id)
    else:
        return redirect("index")

# search_api


def search_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            q = request.POST.get("search")

            return redirect("searched_post", q=q)
    else:
        return redirect("index")


def search_document(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            q = request.POST.get("search")

            return redirect("searched_document", q=q)
    else:
        return redirect("index")


def search_question(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            q = request.POST.get("search")

            return redirect("searched_question", q=q)
    else:
        return redirect("index")

# update_api


def update_document(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Document.objects.filter(id=id).first()
        subject = Subject.objects.filter(edu_rank=post.education_rank).all()
        context = {'post': post, "subjects": subject}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("title")
            post.description = request.POST.get("description")
            post.file = request.FILE.get("file")
            post.image = request.FILE.get("image")
            post.grade = request.POST.get("grade")
            post.price = request.POST.get("price")
            post.subject = request.POST.get("subject")

            post.save()
            return redirect("read_document", id=id)
    else:
        return redirect("index")
    return render("document/update.html", context)


def update_question(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Question.objects.filter(id=id).first()
        subject = Subject.objects.filter(edu_rank=post.education_rank).all()
        context = {'post': post, "subjects": subject}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("title")
            post.description = request.POST.get("description")
            post.file = request.FILE.get("file")
            post.image = request.FILE.get("image")
            post.grade = request.POST.get("grade")
            post.price = request.POST.get("price")
            post.subject = request.POST.get("subject")

            post.save()
            return redirect("read_question", id=id)
    else:
        return redirect("index")
    return render("question/update.html", context)


def update_answer(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Answer.objects.filter(id=id).first()
        context = {'post': post}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("content")
            post.file = request.FILE.get("file")
            post.image = request.FILE.get("image")

            post.save()
            return redirect("read_question", id=post.question.id)
    else:
        return redirect("index")
    return render("question/answer/update.html", context)


def update_post(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Post.objects.filter(id=id).first()
        context = {'post': post}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("content")

            post.save()
            goal = "/post/#"+str(id)
            return redirect(goal)
    else:
        return redirect("index")
    return render("post/update.html", context)


def update_comment_post(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Comment_Post.objects.filter(id=id).first()
        context = {'post': post}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("content")

            post.save()
            goal = "/posts/#"+str(post.post.id)
            return redirect(goal)
    else:
        return redirect("index")
    return render("post/comment/update.html", context)


def update_comment_document(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Comment_Document.objects.filter(id=id).first()
        context = {'post': post}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("content")

            post.save()
            goal = "/document/"+str(post.post.id)+"/#"+str(id)
            return redirect(goal)
    else:
        return redirect("index")
    return render("document/comment/update.html", context)


# read_api


def question_view(request, id):
    if request.user.is_authenticated:
        question = Question.objects.filter(id=id, status="Công khai").first()
        noti = Answer.objects.filter(
            question=question, status="Công khai").all()
        bio = Bio.objects.filter(user=request.user).first()
        context = {'post': question, "answers": noti, "bio": bio}
    else:
        return redirect('check')
    return render(request, 'question/view.html', context)


def post_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Post.objects.filter(id=id).first()
        comment = Comment_Post.objects.filter(post=post).first()
        context = {"bio": bio, "post": post, "comments": comment}
    else:
        return redirect("check")
    return render(request, "post/view.html", context=context)


def document_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        document = Document.objects.filter(id=id, status="Công khai").first()
        check = have_buy_document.objects.filter(
            document=document, user=bio).first()
        noti = Comment_Document.objects.filter(
            post=document, status="Công khai").all()
        context = {'post': document, "comments": noti,
                   'check': check, "bio": bio}
    else:
        return redirect('check')
    return render(request, 'document/view.html', context)


# delete_api
def delete_education_rank(request, id):
    if request.user.is_authenticated:
        education_rank = Education_rank.objects.filter(id=id).first()
        education_rank.delete()
        return redirect("home")
    else:
        return redirect("index")


def delete_user(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        bio.delete()

        user = User.objects.get(username=request.user.username)

        logout(request, request.user)

        user.delete()
    else:
        return redirect("index")


def delete_subject(request, id):
    if request.user.is_authenticated:
        subject = Subject.objects.filter(id=id).first()
        subject.delete()
        return redirect("home")
    else:
        return redirect("index")


def delete_join_cls(request, id):
    if request.user.is_authenticated:
        join_cls = join_cls.objects.filter(id=id).first()
        join_cls.delete()
        return redirect("home")
    else:
        return redirect("index")


def delete_question(request, id):
    if request.user.is_authenticated:
        question = Question.objects.filter(id=id).first()
        question.delete()
        return redirect("question")
    else:
        return redirect("index")


def delete_answer(request, id):
    if request.user.is_authenticated:
        answer = Answer.objects.filter(id=id).first()
        answer.delete()
        return redirect("question_view", id=id)
    else:
        return redirect("index")


def delete_document(request, id):
    if request.user.is_authenticated:
        document = Document.objects.filter(id=id).first()
        document.delete()
        return redirect("document")
    else:
        return redirect("index")


def delete_post(request, id):
    if request.user.is_authenticated:
        post = Post.objects.filter(id=id).first()
        post.delete()
        return redirect("post")
    else:
        return redirect("index")


def delete_comment_Post(request, id):
    if request.user.is_authenticated:
        comment = Comment_Post.objects.filter(id=id).first()
        comment.delete()
        return redirect("post")
    else:
        return redirect("index")


def delete_comment_document(request, id):
    if request.user.is_authenticated:
        comment = Comment_Document.objects.filter(id=id).first()
        comment.delete()
        return redirect("document_view", id=id)
    else:
        return redirect("index")


# user_api


def user_profile(request, id):
    if request.user.is_authenticated:
        your_bio = Bio.objects.filter(user=request.user).first()
        bio = Bio.objects.filter(id=id).first()
        if bio == your_bio:
            return redirect("your_profile")
        else:
            document = Document.objects.filter(
                user=bio, status="Công khai").last()
            post = Post.objects.filter(user=bio, status="Công khai").last()
            question = Question.objects.filter(
                user=bio, status="Công khai").last()

            context = {'user': your_bio, 'document': document,
                       'post': post, 'question': question, 'bio': bio}
    else:
        return redirect("index")
    return render(request, "user/user_profile.html", context)


def your_profile(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()

        # balanced

        # other
        document = Document.objects.filter(user=bio, status="Công khai").last()
        post = Post.objects.filter(user=bio, status="Công khai").last()
        question = Question.objects.filter(user=bio, status="Công khai").last()

        context = {'user': bio, 'document': document, 'post': post,
                   'question': question}
    else:
        return redirect("index")
    return render(request, "user/your_profile.html", context)


def add_social_media(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        if request.method == "POST" and bio:
            bio.facebook = request.POST.get("facebook")
            bio.zalo = request.POST.get("zalo")
            bio.instagram = request.POST.get("instagram")
            bio.twitter = request.POST.get("twitter")

            bio.save()
            return redirect("your_profile")
    else:
        return redirect("index")


def update_profile(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        context = {"user": bio}
        if request.method == "POST":
            bio.user.username = request.POST.get("username")
            bio.user.email = request.POST.get("email")
            bio.user.password = request.POST.get("password")
            bio.grade = request.POST.get("grade")
            bio.education_rank = request.POST.get("edu_rank")
            bio.description = request.POST.get("description")
            bio.avatar = request.FILES['avatar']
            bio.thumnail = request.FILES['thumbnail']
            bio.passcode = request.POST.get("passcode")
            bio.facebook = request.POST.get("facebook")
            bio.zalo = request.POST.get("zalo")
            bio.instagram = request.POST.get("instagram")
            bio.twitter = request.POST.get("twitter")

            bio.save()
    else:
        return redirect("index")
    return render(request, "user/update.html", context)

# apply


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("index")
    else:
        return redirect("index")

# error


def all_error(request):
    return render(request, "error/all_error.html")


# staff_function_view


def staff_index(request):
    if request.user.is_authenticated and request.user.is_staff:
        bio = Bio.objects.filter(user=request.user).first()
        post = Post.objects.filter(status="Chờ kiểm duyệt").count()
        question = Question.objects.filter(status="Chờ kiểm duyệt").count()
        document = Document.objects.filter(status="Chờ kiểm duyệt").count()
        comment_post = Comment_Post.objects.filter(
            status="Chờ kiểm duyệt").count()
        comment_document = Comment_Document.objects.filter(
            status="Chờ kiểm duyệt").count()
        honor = hornorable.objects.filter(status="Chờ xử lý").count()
        answer = Answer.objects.filter(status="Chờ kiểm duyệt").count()
        context = {"post": post, "question": question, "document": document, "honor": honor,
                   "comment_post": comment_post, "comment_document": comment_document, "answer": answer}
    else:
        return redirect("check")
    return render(request, "staff/index.html", context)


def staff_post_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        post = Post.objects.all()
        context = {"posts": post}
    else:
        return redirect("check")
    return render(request, "staff/post.html", context)


def staff_question_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        post = Question.objects.all()
        context = {"questions": post}
    else:
        return redirect("check")
    return render(request, "staff/question.html", context)


def staff_document_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        post = Document.objects.filter(status="Chờ kiểm duyệt").all()
        context = {"documents": post}
    else:
        return redirect("check")
    return render(request, "staff/document.html", context)


def staff_comment_post_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        post = Comment_Post.objects.filter(status="Chờ kiểm duyệt").all()
        context = {"comments": post}
    else:
        return redirect("check")
    return render(request, "staff/comment_post.html", context)


def staff_comment_document_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        post = Comment_Document.objects.filter(status="Chờ kiểm duyệt").all()
        context = {"comments": post}
    else:
        return redirect("check")
    return render(request, "staff/comment_document.html", context)


def staff_answer_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        post = Answer.objects.filter(status="Chờ kiểm duyệt").all()
        context = {"comments": post}
    else:
        return redirect("check")
    return render(request, "staff/answer.html", context)

# staff_function_delete


def staff_delete_post(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Post.objects.filter(id=id).first()
        total = Post.objects.count()
        percent = total * 20 / 100
        bio = Bio.objects.filter(user=post.user.user).first()
        if bio.deleted <= percent:
            bio.user.is_active = False
            bio.user.save()

        post.delete()

        bio.deleted += 1
        bio.save()
        return redirect("staff_post_list")
    else:
        return redirect("check")


def staff_delete_question(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Question.objects.filter(id=id).first()
        total = Question.objects.count()
        percent = total * 20 / 100
        bio = Bio.objects.filter(user=post.user.user).first()
        if bio.deleted <= percent:
            bio.user.is_active = False
            bio.user.save()

        post.delete()

        bio.deleted += 1
        bio.save()
        return redirect("staff_list_question")
    else:
        return redirect("check")


def staff_delete_document(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Document.objects.filter(id=id).first()
        total = Document.objects.count()
        percent = total * 20 / 100
        bio = Bio.objects.filter(user=post.user.user).first()
        if bio.deleted <= percent:
            bio.user.is_active = False
            bio.user.save()

        post.delete()

        bio.deleted += 1
        bio.save()
        return redirect("staff_list_document")
    else:
        return redirect("check")


def staff_delete_comment_post(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Comment_Post.objects.filter(id=id).first()
        total = Comment_Post.objects.count()
        percent = total * 20 / 100
        bio = Bio.objects.filter(user=post.user.user).first()
        if bio.deleted <= percent:
            bio.user.is_active = False
            bio.user.save()

        post.delete()

        bio.deleted += 1
        bio.save()
        return redirect("staff_list_comment_post")
    else:
        return redirect("check")


def staff_delete_answer(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Answer.objects.filter(id=id).first()
        total = Answer.objects.count()
        percent = total * 20 / 100
        bio = Bio.objects.filter(user=post.user.user).first()
        if bio.deleted <= percent:
            bio.user.is_active = False
            bio.user.save()

        post.delete()

        bio.deleted += 1
        bio.save()
        return redirect("staff_list_answer")
    else:
        return redirect("check")


def staff_delete_comment_document(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Comment_Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=post.user.user).first()

        post.delete()

        bio.deleted += 1
        bio.save()
        return redirect("staff_list_comment_document")
    else:
        return redirect("check")

# staff_function_done


def staff_done_post(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Post.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=post.user.user).first()

        post.status = "Công khai"
        post.save()

        return redirect("staff_post_list")
    else:
        return redirect("check")


def staff_done_question(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Question.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=post.user.user).first()

        post.status = "Công khai"
        post.save()
        return redirect("staff_question_list")
    else:
        return redirect("check")


def staff_done_document(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=post.user.user).first()

        post.status = "Công khai"
        post.save()
        return redirect("staff_document_list")
    else:
        return redirect("check")


def staff_done_comment_post(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Comment_Post.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=post.user.user).first()

        post.status = "Công khai"
        post.save()

        post.post.comment_counter += 1
        post.post.save()

        return redirect("staff_comment_post_list")
    else:
        return redirect("check")


def staff_done_answer(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Answer.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=post.user.user).first()

        post.status = "Công khai"
        post.save()

        post.question.comment_counter += 1
        post.question.save()

        return redirect("staff_answer_list")
    else:
        return redirect("check")


def staff_done_comment_document(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Comment_Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=post.user.user).first()

        post.status = "Công khai"
        post.save()

        post.post.comment_counter += 1
        post.post.save()

        return redirect("staff_comment_document_list")
    else:
        return redirect("check")

# staff_function_view


def staff_question_view(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Question.objects.filter(status="Chờ kiểm duyệt", id=id).first()
        context = {"post": post}
    else:
        return redirect("check")
    return render(request, "staff/view/question.html", context)


def staff_document_view(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Document.objects.filter(status="Chờ kiểm duyệt", id=id).first()
        context = {"post": post}
    else:
        return redirect("check")
    return render(request, "staff/view/document.html", context)


def staff_comment_post_view(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Comment_Post.objects.filter(
            status="Chờ kiểm duyệt", id=id).first()
        context = {"post": post}
    else:
        return redirect("check")
    return render(request, "staff/view/comment_post.html", context)


def staff_comment_document_view(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Comment_Document.objects.filter(
            status="Chờ kiểm duyệt", id=id).first()
        context = {"post": post}
    else:
        return redirect("check")
    return render(request, "staff/view/comment_document.html", context)


def staff_answer_view(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        post = Answer.objects.filter(status="Chờ kiểm duyệt", id=id).first()
        context = {"post": post}
    else:
        return redirect("check")
    return render(request, "staff/view/answer.html", context)

# down vote


def down_post(request, id):
    if request.user.is_authenticated:
        post = Post.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        total = Bio.objects.count()
        if bio not in post.down.all():
            post.down.add(bio)
            percent = total * 20 / 100
            if percent <= post.down.count():
                post.status = "Chờ kiểm duyệt"
                post.save()
                return redirect("post")
            else:
                goal = "/posts/#"+str(id)+"/"
                return redirect(goal)
        else:
            post.down.remove(bio)
            goal = "/posts/#"+str(id)+"/"
            return redirect(goal)
    else:
        return redirect("index")


def down_document(request, id):
    if request.user.is_authenticated:
        post = Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        total = Bio.objects.count()
        if bio not in post.down.all():
            post.down.add(bio)
            percent = total * 20 / 100
            if percent <= post.down.count():
                post.status = "Chờ kiểm duyệt"
                post.save()
                return redirect("document")
            else:
                return redirect("read_document", id=post.id)
        else:
            post.down.remove(bio)
            return redirect("document_view", id=id)
    else:
        return redirect("index")


def down_comment_post(request, id):
    if request.user.is_authenticated:
        post = Comment_Post.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        total = Bio.objects.count()
        if bio not in post.down.all():
            post.down.add(bio)
            percent = total * 20 / 100
            if percent <= post.down.count():
                post.status = "Chờ kiểm duyệt"
                post.save()
                return redirect("post")
            else:
                goal = "/posts/#"+str(id)+"/"
                return redirect(goal)
        else:
            post.down.remove(bio)
            goal = "/posts/#"+str(id)+"/"
            return redirect(goal)
    else:
        return redirect("index")


def down_comment_document(request, id):
    if request.user.is_authenticated:
        post = Comment_Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        total = Bio.objects.count()
        if bio not in post.down.all():
            post.down.add(bio)
            percent = total * 20 / 100
            if percent <= post.down.count():
                post.status = "Chờ kiểm duyệt"
                post.save()
                return redirect("document")
            else:
                return redirect("read_document", id=post.id)
        else:
            post.down.remove(bio)
            return redirect("document_view", id=id)
    else:
        return redirect("index")


def down_question(request, id):
    if request.user.is_authenticated:
        post = Question.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        total = Bio.objects.count()
        if bio not in post.down.all():
            post.down.add(bio)
            percent = total * 20 / 100
            if percent <= post.down.count():
                post.status = "Chờ kiểm duyệt"
                post.save()
                return redirect("question")
            else:
                return redirect("read_question", id=post.id)
        else:
            post.down.remove(bio)
            return redirect("read_question", id=id)
    else:
        return redirect("index")


def down_answer(request, id):
    if request.user.is_authenticated:
        post = Answer.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        total = Bio.objects.count()
        if bio not in post.down.all():
            post.down.add(bio)
            percent = total * 20 / 100
            if percent <= post.down.count():
                post.status = "Chờ kiểm duyệt"
                post.save()
                return redirect("question")
            else:
                return redirect("read_question", id=post.question.id)
        else:
            post.down.remove(bio)
            return redirect("read_question", id=post.question.id)
    else:
        return redirect("index")

# download_file


def download_document_file(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        document = Document.objects.filter(id=id).first()
        if document.price >= 1:
            check = have_buy_document.objects.filter(
                document=document, user=bio).first()
            if bio and check:
                response = HttpResponse(document.file)
                response['Content-Type'] = 'application/force-download'
                response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
                return response
        else:
            response = HttpResponse(document.file)
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
            return response
        return redirect("document_view", id=id)


def download_question_file(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        document = Question.objects.filter(id=id).first()
        if bio and document:
            response = HttpResponse(document.file)
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
            return response
        return redirect("question_view", id=id)


def staff_download_document_file(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        document = Document.objects.filter(id=id).first()
        if bio and document:
            response = HttpResponse(document.file)
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
            return response
        return redirect("staff_document_view", id=id)


def download_answer_file(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        document = Answer.objects.filter(id=id).first()
        if bio and document:
            response = HttpResponse(document.file)
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
            return response
        return redirect("question_view", id=document.question.id)

# bill


def post_bill(request, value, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Post.objects.filter(id=id).first()
        if bio and post:
            context = {"post": post, "bio": bio, "value": value}
        else:
            return redirect("all_error")
    else:
        return redirect("index")
    return render(request, "post/bill.html", context)


def document_bill(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Document.objects.filter(id=id).first()
        if bio and post:
            context = {"post": post, "bio": bio}
        else:
            return redirect("all_error")
    else:
        return redirect("index")
    return render(request, "document/bill.html", context)


def question_bill(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Answer.objects.filter(id=id).first()
        if bio and post:
            context = {"post": post, "bio": bio}
        else:
            return redirect("all_error")
    else:
        return redirect("index")
    return render(request, "question/bill.html", context)


def success(request, status):
    if request.user.is_authenticated:
        return render(request, "success.html", context={"status": status})
    else:
        return redirect("check")


def check_question(request, id):
    if request.user.is_authenticated:
        post = Answer.objects.filter(id=id).first()
        if post.question.price == 0:
            post.question.answered = 1
            post.question.save()

            post.choosen = 1
            post.save()
            return redirect("question_view", id=post.question.id)
        else:
            return redirect("all_error")
    else:
        return redirect("check")

# GPTeen


def gpteen_input(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        if bio.balance >= 10 and request.method == "POST":
            prompt = request.POST.get("gpteen")
            return redirect("gpteen_answer_result", prompt=str(prompt))
    else:
        return redirect("index")


def gpteen_answer(request, prompt):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        if bio.balance >= 10 and prompt:
            bio.balance -= 10
            bio.save()
            result = GPTeen(prompt=prompt)
            context = {"result": result[8:-4], "bio": bio}
        else:
            return redirect("all_error")
    else:
        return redirect("all_error")
    return render(request, "GPTeen/result.html", context)

# quản lý từ khóa bẩn


def add_bad_keyword(request):
    if request.user.is_authenticated and request.user.is_staff:
        keyword = request.POST.get("keyword")

        new_keyword = bad_keyword(keyword=keyword, status="Cấm")
        new_keyword.save()
    else:
        return redirect("index")
    return render(request, "staff/bad_word.html")


def staff_check_all_bad_keyword(request):
    if request.user.is_authenticated and request.user.is_staff:
        bad = bad_keyword.objects.all()
        bio = Bio.objects.filter(user=request.user).first()
        context = {"posts": bad, "bio": bio}
    else:
        return redirect("index")
    return render(request, "staff/view/bad_word.html", context)


def staff_ban_suggest_bad_keyword(request, keyword):
    if request.user.is_authenticated and request.user.is_staff:
        bad = bad_keyword.objects.filter(
            keyword=keyword, status="Chờ xem xét").first()
        bad.status = "Cấm"
        bad.save()
        # bio = Bio.objects.filter(user=request.user).first()
    else:
        return redirect("index")


def staff_delete_suggest_bad_keyword(request, keyword):
    if request.user.is_authenticated and request.user.is_staff:
        bad = bad_keyword.objects.filter(
            keyword=keyword, status="Chờ xem xét").first()
        bad.delete()
        # bio = Bio.objects.filter(user=request.user).first()
    else:
        return redirect("index")


def staff_delete_ban_bad_keyword(request, keyword):
    if request.user.is_authenticated and request.user.is_staff:
        bad = bad_keyword.objects.filter(keyword=keyword, status="Cấm").first()
        bad.delete()
        # bio = Bio.objects.filter(user=request.user).first()
    else:
        return redirect("index")


def suggest_bad_keyword(request):
    if request.user.is_authenticated:
        keyword = request.POST.get("keyword")

        new_keyword = bad_keyword(keyword=keyword, status="Chờ xem xét")
        new_keyword.save()
    else:
        return redirect("index")
    return render(request, "user/bad_word.html")


# vinh danh
def user_honor(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        honor = hornorable.objects.filter(user=bio).all()
        context = {"bio": bio, "honor": honor[::-1]}
    else:
        return redirect("index")
    return render(request, "user/honor.html", context)


def staff_all_honor(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        honor = hornorable.objects.all()
        context = {"bio": bio, "posts": honor[::-1]}
    else:
        return redirect("index")
    return render(request, "staff/view/honor.html", context)


def staff_check_honor(request, id):
    if request.user.is_authenticated:
        honor = hornorable.objects.filter(id=id).first()
        honor.status = "Đã vinh danh"
        honor.save()
        return redirect("staff_honor")
    else:
        return redirect("index")

# quiz


def make_quiz(request):
    if request.user.is_authenticated and request.user.is_staff:
        subject = Subject.objects.all()
        edu_rank = Education_rank.objects.all()
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            number_of_question = request.POST.get("number_of_question")
            grade = request.POST.get("grade")
            subject = request.POST.get("subject")
            edu_rank = request.POST.get("edu_rank")
            image = request.FILES.get("image")

            bio = Bio.objects.filter(user=request.user).first()
            subject = Subject.objects.filter(id=subject).first()
            edu_rank = Education_rank.objects.filter(id=edu_rank).first()
            sql = Quiz(name=title, description=description, grade=grade, number_of_question=number_of_question,
                       subject=subject, edu_rank=edu_rank, image=image, user=bio)
            sql.save()
            return redirect("make_question", quiz_id=sql.id, ques_no=1)
    else:
        return redirect("index")
    return render(request, "quiz/create.html", context={"subjects": subject, "edu_ranks": edu_rank})


def make_question(request, quiz_id, ques_no):
    if request.user.is_authenticated and request.user.is_staff:
        bio = Bio.objects.filter(user=request.user).first()
        quiz = Quiz.objects.filter(id=quiz_id).first()
        if quiz.user == bio:
            ques = Quiz_questions.objects.filter(
                quiz=quiz, number=ques_no).first()
            if ques:
                return redirect("edit_question", quiz_id=quiz_id, ques_no=ques_no)
            else:
                if request.method == "POST":
                    name = request.POST.get("title")
                    a = request.POST.get("ans_a")
                    b = request.POST.get("ans_b")
                    c = request.POST.get("ans_c")
                    d = request.POST.get("ans_d")
                    correct_answer = request.POST.get("correct_answer")

                    sql = Quiz_questions(
                        name=name, number=ques_no, quiz=quiz, a=a, b=b, c=c, d=d, correct=correct_answer)
                    sql.save()

                    if ques_no == quiz.number_of_question:
                        return redirect("quiz")
                    else:
                        return redirect("make_question", quiz_id=quiz_id, ques_no=ques_no+1)
        else:
            return redirect("all_error")
    else:
        return redirect("index")
    return render(request, "quiz/question/create.html")


def edit_question(request, quiz_id, ques_no):
    if request.user.is_authenticated and request.user.is_staff:
        bio = Bio.objects.filter(user=request.user).first()
        quiz = Quiz.objects.filter(id=quiz_id).first()
        if quiz.user == bio:
            ques = Quiz_questions.objects.filter(
                quiz=quiz, number=ques_no).first()
            if ques:
                if request.method == "POST":
                    name = request.POST.get("name")
                    a = request.POST.get("ans_a")
                    b = request.POST.get("ans_b")
                    c = request.POST.get("ans_c")
                    d = request.POST.get("ans_d")
                    correct_answer = request.POST.get("correct_answer")

                    sql = Quiz_questions(
                        name=name, number=ques_no, quiz=quiz, a=a, b=b, c=c, d=d, correct=correct_answer)
                    sql.save()

                    if ques_no == quiz.number_of_question:
                        return redirect("quiz")
                    else:
                        return redirect("make_question", quiz_id=sql.id, ques_no=ques_no+1)
            else:
                return redirect("make_question", quiz_id=quiz_id, ques_no=ques_no)
        else:
            return redirect("all_error")
    else:
        return redirect("index")
    return render(request, "quiz/question/create.html")


def delete_quiz(request, id):
    bio = Bio.objects.filter(user=request.user).first()
    quiz = Quiz.objects.filter(id=id).first()
    if request.user.is_authenticated and request.user.is_staff and bio == quiz.user:
        quiz.delete()
        return redirect("quiz")
    else:
        return redirect("index")


def delete_question(request, id):
    bio = Bio.objects.filter(user=request.user).first()
    quiz = Quiz_questions.objects.filter(id=id).first()
    if request.user.is_authenticated and request.user.is_staff and bio == quiz.user:
        quiz.quiz.number_of_question -= 1
        quiz.quiz.save()
        quiz.delete()
        return redirect("quiz")
    else:
        return redirect("index")


def quiz_list(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        quiz = Quiz.objects.all()
        context = {"bio": bio, "posts": quiz}
    else:
        return redirect("index")
    return render(request, "quiz/list.html", context=context)


def quiz_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        quiz = Quiz.objects.filter(id=id).first()
        question = Quiz_questions.objects.filter(number=1, quiz=quiz).first()
        context = {"bio": bio, "post": quiz, "question": question}
    else:
        return redirect("index")
    return render(request, "quiz/view.html", context)


def quiz_question_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        ques = Quiz_questions.objects.filter(id=id).first()
        context = {"bio": bio, "question": ques}
        if request.method == "POST":
            answer = request.POST.get("answer")
            check = "Sai"
            plus = 0
            if answer == ques.correct:
                check = "Đúng"
                plus = random.randint(1, 100)
                bio.balance += plus
                bio.save()
            return redirect("quiz_question_after_view", status=check, point=plus, id=id)
    else:
        return redirect("index")
    return render(request, "quiz/question/view.html", context=context)


def quiz_question_after_view(request, status, point, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        ques = Quiz_questions.objects.filter(id=id).first()
        next_ques = Quiz_questions.objects.filter(
            number=ques.number+1, quiz=ques.quiz).first()
        if next_ques:
            context = {"bio": bio, "status": status,
                       "point": point, "next_question": next_ques.id, "ques": ques}
        else:
            context = {"bio": bio, "status": status,
                       "point": point, "next_question": False, "ques": ques}
    else:
        return redirect("index")
    return render(request, "quiz/question/result.html", context=context)


def GPTeen_image(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        if request.method == "POST":
            image = request.POST.get("image")
            sql = GPTeen_doc(image=image)
            sql.save()
            return redirect("gpteen_image_result", id=sql.id)
    else:
        return redirect("check")


def GPTeen_image_result(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        gpteen_image = GPTeen_doc.objects.filter(id=id).first()
        if bio and gpteen_image.image:
            result = search_image(url=gpteen_image.image.url)
            bio.balance -= 50
            bio.save()
            context = {"bio": bio, "result": result[8:-4]}
        else:
            return redirect("check")
    else:
        return redirect("check")
    return render(request, "gpteen/image/result.html", context=context)


def GPTeen_document(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        if request.method == "POST":
            doc = request.POST.get("doc")
            sql = GPTeen_doc(doc=doc)
            sql.save()
            return redirect("gpteen_document_result", id=sql.id)
    else:
        return redirect("check")


def GPTeen_document_result(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        gpteen_doc = GPTeen_doc.objects.filter(id=id).first()
        if bio and gpteen_doc.doc:
            result = search_document(url=gpteen_doc.doc.url)
            bio.balance -= 50
            bio.save()
            context = {"bio": bio, "result": result[8:-4]}
        else:
            return redirect("check")
    else:
        return redirect("check")
    return render(request, "gpteen/document/result.html", context=context)


def GPTeen_university(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        if request.method == "POST":
            total_score = request.POST.get("total_score")
            category_code = request.POST.get("category_code")
            job = request.POST.get("job")
            area = request.POST.get("area")
            return redirect("gpteen_university_result", score=total_score, category_code=category_code, job=job, area=area)
    else:
        return redirect("check")


def GPTeen_university_result(request, score, category_code, job, area):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        # gpteen_doc = GPTeen_University_doc.objects.filter(id=id).first()
        if bio:
            result = gptu_check(
                score=score, category_code=category_code, job=job, area=area)
            bio.balance -= 100
            bio.save()
            context = {"bio": bio, "result": result}
        else:
            return redirect("check")
    else:
        return redirect("check")
    return render(request, "gpteen/university/result.html", context=context)
