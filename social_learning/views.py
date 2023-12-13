"""
Còn nhiều function chx đc add vào. Khi nào team hội ý và thống nhất đc thì add vào sau.
"""

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from .hashed import hashed, create_private_key, create_account
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
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import hashlib
import os
import pyperclip as clip

web3 = Web3(Web3.HTTPProvider(
    'https://sepolia.infura.io/v3/8c4c9235b7ed489ab0bc8c26795ae24e'))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"tokens","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeSub","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeDiv","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeMul","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeAdd","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"tokenOwner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Approval","type":"event"}]')
contract = web3.eth.contract(
    address='0x2519019C7251545be7B81521951874B2c4948A56', abi=abi)

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
            user = User.objects.get(username=username)
            edu = Education_rank.objects.get(id=education_rank)
            if user and edu:
                key = create_private_key()
                wallet = create_account(key)
                passcode = hashed(passcode)
                bio = Bio(user=user, avatar=avatar, thumbnail=thumbnail, grade=grade, edu_rank=edu,
                          description=description, address=wallet, address_password=key, wallet_passcode=passcode)
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

                key = create_private_key()
                wallet = create_account(key)

                passcode = hashed(passcode)
                bio = Bio(user=request.user, avatar=avatar, thumbnail=thumbnail, grade=grade, edu_rank=edu,
                          description=description, address=wallet, address_password=key, wallet_passcode=passcode)
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

# searched_list_view


def searched_question_list_view(request, q):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        post = Question.objects.filter(Q(title__icontain=q) | Q(
            description__icontain=q), grade__lte=user.grade).all()
        context = {"posts": post[::-1]}
    else:
        return redirect("index")
    return render(request, "question/list.html", context)


def searched_gigs_list_view(request, q):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        post = Gigs.objects.filter(Q(title__icontain=q) | Q(
            description__icontain=q), grade__lte=user.grade, education_rank=user.edu_rank).all()
        context = {"posts": post[::-1]}
    else:
        return redirect("index")
    return render(request, "gigs/list.html", context)


def searched_document_list_view(request, q):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        post = Document.objects.filter(Q(title__icontain=q) | Q(
            description__icontain=q), grade__lte=user.grade, edu_rank=user.edu_rank).all()
        context = {"posts": post[::-1]}
    else:
        return redirect("index")
    return render(request, "document/list.html", context)


def searched_post_list_view(request, q):
    if request.user.is_authenticated:
        post = Post.objects.filter(Q(content__icontain=q)).all()
        context = {"posts": post[::-1]}
    else:
        return redirect("index")
    return render(request, "document/list.html", context)


def searched_trade_list_view(request, q):
    if request.user.is_authenticated:
        post = Trade.objects.filter(
            Q(title__icontain=q) | Q(description__icontain=q)).all()
        context = {"posts": post[::-1]}
    else:
        return redirect("index")
    return render(request, "trade/list_view.html", context)

# list_view


def question_list_view(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        teen = float(Web3.to_wei(
            contract.functions.balanceOf(bio.address).call(), 'wei') / 1000000000000000000)

        edu_rank = Education_rank.objects.all()
        subject = Subject.objects.all()

        post = Question.objects.filter(grade__lte=bio.grade).all()
        context = {"posts": post[::-1], 'teen': teen,
                   'subjects': subject, 'educations': edu_rank}
    else:
        return redirect("index")
    return render(request, "question/list.html", context)


def gigs_list_view(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        teen = float(Web3.to_wei(
            contract.functions.balanceOf(bio.address).call(), 'wei') / 1000000000000000000)

        edu_rank = Education_rank.objects.all()
        subject = Subject.objects.all()

        post = Gigs.objects.filter(
            grade__lte=bio.grade, education_rank=bio.edu_rank).all()
        context = {"posts": post[::-1], 'teen': teen,
                   'subjects': subject, 'educations': edu_rank, "bio": bio}
    else:
        return redirect("index")
    return render(request, "gigs/list.html", context)


def document_list_view(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        teen = float(Web3.to_wei(
            contract.functions.balanceOf(bio.address).call(), 'wei') / 1000000000000000000)

        edu_rank = Education_rank.objects.all()
        subject = Subject.objects.all()

        post = Document.objects.filter(
            grade__lte=bio.grade, edu_rank=bio.edu_rank).all()
        context = {"posts": post[::-1], 'teen': teen,
                   'subjects': subject, 'educations': edu_rank}
    else:
        return redirect("index")
    return render(request, "document/list.html", context)


def post_list_view(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        address = str(bio.address)
        teen = contract.functions.balanceOf(
            address).call()
        post = Post.objects.all()
        context = {"posts": post[::-1],
                   'teen': float(web3.to_wei(teen, 'wei') / 1000000000000000000)}
    else:
        return redirect("index")
    return render(request, "post/list.html", context)


def trade_list_view(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        teen = float(web3.to_wei(
            contract.functions.balanceOf(bio.address).call(), 'wei') / 1000000000000000000)

        currency = payment_method.objects.all()
        post = Trade.objects.all()
        context = {"posts": post[::-1], 'teen': teen, 'currencies': currency}
    else:
        return redirect("index")
    return render(request, "trade/list.html", context)

# create_api


def post_create(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        if request.method == "POST":
            content = request.POST.get("content")
            sql = Post(content=content, user=user, comment_counter=0)
            sql.save()
            return redirect("post")
    else:
        return redirect("index")


def document_create(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            image = request.FILES.get("image")
            file = request.POST.get('file')
            grade = request.POST.get("grade")
            price = request.POST.get("price")
            edu_rank = request.POST.get("education_rank")
            subject = request.POST.get("subject")

            edu_rank = Education_rank.objects.get(id=edu_rank)
            subject = Subject.objects.get(id=subject)

            sql = Document(title=title, description=description, file=file, image=image,
                           grade=grade, edu_rank=edu_rank, user=user, price=price, subject=subject, comment_counter=0)
            sql.save()
            return redirect("document")
    else:
        return redirect("index")


def gigs_create(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            result = request.POST.get("result")
            image = request.FILES.get("image")
            grade = request.POST.get("grade")
            edu_rank = request.POST.get("education_rank")
            book = request.POST.get("book_include")
            type_learn = request.POST.get("type_learn")
            subject = request.POST.get("subject")
            price = request.POST.get("price")

            edu_rank = Education_rank.objects.get(id=edu_rank)
            subject = Subject.objects.get(id=subject)

            sql = Gigs(title=title, result=result, price=price, subject=subject, description=description,
                       book_include=book, type_learn=type_learn, image=image, grade=grade, education_rank=edu_rank, user=user, comment_counter=0)
            sql.save()
            return redirect("gigs")
    else:
        return redirect("index")


def question_create(request):
    if request.user.is_authenticated:
        user = Bio.objects.get(user=request.user)
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            file = request.POST.get("file")
            image = request.FILES.get("image")
            grade = request.POST.get("grade")
            edu_rank = request.POST.get("education_rank")
            subject = request.POST.get("subject")
            price = int(request.POST.get("price"))

            if price <= 1:
                price = 1

            edu_rank = Education_rank.objects.filter(id=edu_rank).first()
            subject = Subject.objects.filter(id=subject).first()

            sql = Question(title=title, description=description, price=price, file=file,
                           subject=subject, image=image, grade=grade, education_rank=edu_rank, user=user, answered=0, comment_counter=0)
            sql.save()

            sql = Question.objects.get(title=title, description=description, price=price, file=file,
                                       subject=subject, image=image, grade=grade, education_rank=edu_rank, user=user, answered=0, comment_counter=0)
            return redirect("question_view", id=sql.id)
    else:
        return redirect("index")


def create_trade_offer(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        if request.method == "POST":
            change_value = int(request.POST.get("change_value"))
            change_currency = request.POST.get("change_currency")
            changed_currency = request.POST.get("changed_currency")

            if change_currency and change_value and changed_currency:

                change_currency = payment_method.objects.filter(
                    id=change_currency).first()
                changed_currency = payment_method.objects.filter(
                    id=changed_currency).first()

                if change_currency.name == "Teen" and changed_currency.name == "ETH":
                    changed_value = 0.22 * change_value
                elif changed_currency.name == "Teen" and change_currency.name == "ETH":
                    changed_value == changed_value / 0.22
                elif changed_currency.name == change_currency.name:
                    changed_currency = payment_method.objects.filter(
                        name="Khác").first()
                    change_currency = payment_method.objects.filter(
                        name="Teen").first()
                    changed_value = 10000 * change_value
                else:
                    changed_value = 10000 * changed_value

                sql = Trade(change_value=change_value, changed_value=changed_value, change_currency=change_currency,
                            changed_currency=changed_currency, payment_method=changed_currency, done="Còn hạn", user=bio)
                sql.save()

                sql2 = Trade.objects.filter(change_value=change_value, changed_value=changed_value, change_currency=change_currency,
                                            changed_currency=changed_currency, payment_method=changed_currency, done="Còn hạn", user=bio).first()

                return redirect("trade")
            else:
                return redirect("post")
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
                    return redirect("question_view", id=id)
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

                    goal = str(document.file)
                    print(goal)
                    return redirect(goal)
                else:
                    return redirect("all_error")
            else:
                return redirect("all_error")
    else:
        return redirect("index")


def gigs_payment(request, id):
    if request.user.is_authenticated:
        gigs = join_cls.objects.filter(id=id).first()
        if request.method == "POST" and gigs:
            code = request.POST.get("code")

            final = hashed(code)
            if final != "ValueError: The passcode just contain only number from 0 to 9":
                bio = Bio.objects.filter(
                    wallet_passcode=final, user=request.user).first()

                teen_balanced = float(web3.to_wei(
                    contract.functions.balanceOf(bio.address).call(), 'ether'))

                if bio.id == gigs.student.id:

                    if final == bio.wallet_passcode and teen_balanced >= gigs.gig.price:
                        learn = Learn.objects.filter(
                            check_stu=gigs).last()
                        if learn:

                            os.environ["real_password_gigs" +
                                       bio.user.username] = bio.address_password
                            real_password = os.getenv(
                                "real_password_gigs"+bio.user.username)

                            tran = contract.functions.transfer(gigs.gig.user.address, web3.to_wei(gigs.gig.price, 'ether')).build_transaction(
                                {'chainId': 11155111, 'gas': 2163200, 'nonce': web3.eth.get_transaction_count(bio.address), 'value': 0})
                            signed_txn = web3.eth.account.sign_transaction(
                                tran, real_password)
                            web3.eth.send_raw_transaction(
                                signed_txn.rawTransaction)
                            return redirect("payment_bill", id=id)
                        else:
                            return redirect("all_error")

            else:
                return redirect("all_error")
    else:
        return redirect("index")
    return render(request, "gigs/code_submit.html")

# trade_api


def eth_to_teen(request, id):
    if request.user.is_authenticated:
        post = Trade.objects.filter(id=id).first()
        if request.method == "POST" and post and post.change_currency.name == "ETH" and post.changed_currency.name == "Teen":
            code = request.POST.get("passcode")
            if code:
                final = hashed(code)
                if final != "ValueError: The passcode just contain only number from 0 to 9":
                    bio = Bio.objects.filter(
                        wallet_passcode=final, user=request.user).first()
                    teen_balanced = float(web3.to_wei(
                        contract.functions.balanceOf(bio.address).call(), 'ether'))
                    eth_balanced = float(eth_balanced=float(web3.to_wei(
                        web3.eth.get_balance(post.user.address), 'ether')))
                    if teen_balanced >= post.changed_value and eth_balanced >= post.change_value:
                        os.environ["real_password_teen" +
                                   bio.user.username] = bio.address_password
                        real_password = os.getenv(
                            "real_password_teen"+bio.user.username)

                        tran = contract.functions.transfer(post.user.address, web3.to_wei(post.changed_price, 'ether')).build_transaction(
                            {'chainId': 11155111, 'gas': 2163200, 'nonce': web3.eth.get_transaction_count(bio.address), 'value': 0})
                        signed_txn = web3.eth.account.sign_transaction(
                            tran, real_password)
                        web3.eth.send_raw_transaction(
                            signed_txn.rawTransaction)

                        os.environ["real_password_eth" +
                                   post.user.username] = post.user.address_password
                        test2 = os.getenv(
                            "real_password_eth"+post.user.username)
                        tran = {'chainId': 11155111, 'gas': 2163200, 'nonce': web3.eth.get_transaction_count(
                            post.user.address), 'to': bio.address, 'value': web3.to_wei(post.change_value, 'ether')}
                        signed_txn = web3.eth.account.sign_transaction(
                            tran, test2)
                        web3.eth.send_raw_transaction(
                            signed_txn.rawTransaction)
                        return redirect("/trade/#"+str(id))
                    else:
                        return redirect("all_error")
                else:
                    return redirect("all_error")
            else:
                return redirect("index")


def teen_to_eth(request, id):
    if request.user.is_authenticated:
        post = Trade.objects.filter(id=id).first()
        if request.method == "POST" and post and post.change_currency.name == "Teen" and post.changed_currency.name == "ETH":
            code = request.POST.get("passcode")
            if code:
                final = hashed(code)
                if final != "ValueError: The passcode just contain only number from 0 to 9":
                    bio = Bio.objects.filter(
                        wallet_passcode=final, user=request.user).first()
                    teen_balanced = float(web3.to_wei(
                        contract.functions.balanceOf(bio.address).call(), 'ether'))
                    eth_balanced = float(eth_balanced=float(web3.to_wei(
                        web3.eth.get_balance(post.user.address), 'ether')))
                    if teen_balanced >= post.changed_value and eth_balanced >= post.change_value:
                        post.done = "Đã Hoàn Thành Giao Dịch"
                        post.save()

                        os.environ["real_password_teen" +
                                   bio.user.username] = bio.address_password
                        real_password = os.getenv(
                            "real_password_teen"+bio.user.username)

                        tran = contract.functions.transfer(bio.address, web3.to_wei(post.changed_price, 'ether')).build_transaction(
                            {'chainId': 11155111, 'gas': 2163200, 'nonce': web3.eth.get_transaction_count(bio.address), 'value': 0})
                        signed_txn = web3.eth.account.sign_transaction(
                            tran, real_password)
                        web3.eth.send_raw_transaction(
                            signed_txn.rawTransaction)

                        os.environ["real_password_eth" +
                                   post.user.username] = post.user.address_password
                        test2 = os.getenv(
                            "real_password_eth"+post.user.username)
                        tran = {'chainId': 11155111, 'gas': 2163200, 'nonce': web3.eth.get_transaction_count(
                            post.user.address), 'to': bio.address, 'value': web3.to_wei(post.change_value, 'ether')}
                        signed_txn = web3.eth.account.sign_transaction(
                            tran, test2)
                        web3.eth.send_raw_transaction(
                            signed_txn.rawTransaction)
                        return redirect("/trade/#"+str(id))
                    else:
                        return redirect("all_error")
                else:
                    return redirect("all_error")
            else:
                return redirect("index")

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
            return redirect("read_document", id=id)
        else:
            post.like.remove(bio)
            return redirect("read_document", id=id)
    else:
        return redirect("index")


def like_document(request, id):
    if request.user.is_authenticated:
        post = Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if not bio in post.like.all():
            post.like.add(bio)
            return redirect("read_document", id=id)
        else:
            post.like.remove(bio)
            return redirect("read_document", id=id)
    else:
        return redirect("index")


def like_gig(request, id):
    if request.user.is_authenticated:
        post = Gigs.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if not bio in post.like.all():
            post.like.add(bio)
            return redirect("read_gig", id=id)
        else:
            post.like.remove(bio)
            return redirect("read_gig", id=id)
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


def dislike_gig(request, id):
    if request.user.is_authenticated:
        post = Gigs.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if bio not in post.dislike.all:
            post.dislike.add(bio)
            return redirect("read_gig", id=id)
        else:
            post.dislike.remove(bio)
            return redirect("read_gig", id=id)
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
        comments = Comment_Post.objects.filter(post__id=id, reply=None).all()
        post = Post.objects.filter(id=id).first()
        context = {'comments': comments, 'post': post}
    else:
        return redirect("index")
    return render(request, "post/comment_view.html", context)


def comment_post(request, id):
    if request.user.is_authenticated:
        post = Post.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method == "POST":
                content = request.POST.get("content")

                sql = Comment_Post(post=post, user=bio, content=content)
                sql.save()
                post.comment_counter += 1
                post.save()
                sql = Comment_Post.objects.filter(
                    post=post, user=bio, content=content).first()

                goal = "/view/comment/post/"+str(id)+"/#"+str(sql.id)+"/"
                return redirect(goal)
        else:
            return redirect("read_post", id=id)
    else:
        return redirect("index")


def comment_gig(request, id):
    if request.user.is_authenticated:
        post = Gigs.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method == "POST":
                content = request.POST.get("content")

                sql = Comment_Gigs(post=post, user=bio, content=content)
                sql.save()

                post.comment_counter += 1
                post.save()

                sql = Comment_Gigs.objects.filter(
                    post=post, user=bio, content=content).first()
                goal = "/gig/"+str(id)+"/#"+str(sql.id)+"/"
                return redirect(goal)
        else:
            return redirect("read_gig", id=id)
    else:
        return redirect("index")


def comment_document(request, id):
    if request.user.is_authenticated:
        post = Document.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method == "POST":
                content = request.POST.get("content")

                sql = Comment_Document(post=post, user=bio, content=content)
                sql.save()

                post.comment_counter += 1
                post.save()

                sql = Comment_Document.objects.filter(
                    post=post, user=bio, content=content).first()
                goal = "/document/"+str(id)+"/#"+str(sql.id)+"/"
                return redirect(goal)
        else:
            return redirect("gig_view", id=id)
    else:
        return redirect("index")


def answer(request, id):
    if request.user.is_authenticated:
        post = Question.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method == "POST":
                content = request.POST.get("content")
                file = request.POST.get("file")
                image = request.FILES.get("image")

                sql = Answer(question=post, user=bio,
                             content=content, image=image, file=file, choosen=0)
                sql.save()

                post.comment_counter += 1
                post.save()

                sql = Answer.objects.filter(
                    question=post, user=bio, content=content, image=image, file=file, choosen=0).first()
                goal = "/question/"+str(id)+"/#"+str(sql.id)+"/"
                return redirect(goal)
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

                p.comment_counter += 1
                p.save()

                sql = Comment_Post.objects.filter(
                    post=post.post, user=bio, content=content, reply=post).first()
                goal = "/view/comment/post/"+str(p.id)+"/#"+str(sql.id)+"/"
                return redirect(goal)
        else:
            return redirect("read_post", id=id)
    else:
        return redirect("index")


def reply_comment_gig(request, id):
    if request.user.is_authenticated:
        post = Comment_Gigs.objects.filter(id=id).first()
        bio = Bio.objects.filter(user=request.user).first()
        if post and bio:
            if request.method == "POST":
                content = request.POST.get("content")

                sql = Comment_Gigs(post=post.post, user=bio,
                                   content=content, reply=post)
                sql.save()

                post.comment_counter += 1
                post.save()

                sql = Comment_Gigs.objects.filter(
                    post=post.post, user=bio, content=content, reply=post).first()
                goal = "/gig/"+str(id)+"/#"+str(sql.id)+"/"
                return redirect(goal)
        else:
            return redirect("read_gig", id=id)
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


def search_gig(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            q = request.POST.get("search")

            return redirect("searched_gig", q=q)
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


def update_gig(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Gigs.objects.filter(id=id).first()
        subject = Subject.objects.filter(edu_rank=post.education_rank).all()
        context = {'post': post, "subjects": subject}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("title")
            post.description = request.POST.get("description")
            post.result = request.POST.get("result")
            post.image = request.FILE.get("image")
            post.grade = request.POST.get("grade")
            post.price = request.POST.get("price")
            post.subject = request.POST.get("subject")
            post.book_include = request.POST.get("book_include")
            post.type_learn = request.POST.get("type_learn")

            post.save()
            return redirect("read_gig", id=id)
    else:
        return redirect("index")
    return render("gigs/update.html", context)


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


def update_comment_gigs(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Comment_Gigs.objects.filter(id=id).first()
        context = {'post': post}
        if request.method == "POST" and post and bio:
            post.title = request.POST.get("content")

            post.save()
            goal = "/gig/"+str(post.post.id)+"/#"+str(id)
            return redirect(goal)
    else:
        return redirect("index")
    return render("gigs/comment/update.html", context)


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
def gigs_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.get(user=request.user)
        gigs = Gigs.objects.filter(id=id).first()
        noti = Comment_Gigs.objects.filter(post=gigs).all()
        context = {'post': gigs, "notis": noti, 'bio': bio}
    else:
        return redirect('a_login')
    return render(request, 'gigs/view.html', context)


def question_view(request, id):
    if request.user.is_authenticated:
        question = Question.objects.filter(id=id).first()
        noti = Answer.objects.filter(question=question).all()
        context = {'post': question, "answers": noti}
    else:
        return redirect('a_login')
    return render(request, 'question/view.html', context)


def document_view(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        document = Document.objects.filter(id=id).first()
        check = have_buy_document.objects.filter(
            document=document, user=bio).first()
        noti = Comment_Document.objects.filter(post=document).all()
        context = {'post': document, "comments": noti, 'check': check}
    else:
        return redirect('a_login')
    return render(request, 'document/view.html', context)


def post_view(request, id):
    if request.user.is_authenticated:
        post = Post.objects.filter(id=id).first()
        noti = comment_post.objects.filter(post=post).all()
        context = {'post': post, "notis": noti}
    else:
        return redirect('a_login')
    return render(request, 'post/view.html', context)


# delete_api
def delete_education_rank(request, id):
    if request.user.is_authenticated:
        education_rank = education_rank.objects.filter(id=id).first()
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
        subject = subject.objects.filter(id=id).first()
        subject.delete()
        return redirect("home")
    else:
        return redirect("index")


def delete_gigs(request, id):
    if request.user.is_authenticated:
        gigs = gigs.objects.filter(id=id).first()
        gigs.delete()
        return redirect("home")
    else:
        return redirect("index")


def delete_comment_gig(request, id):
    if request.user.is_authenticated:
        comment = comment_gig.objects.filter(id=id).first()
        comment.delete()
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
        question = question.objects.filter(id=id).first()
        question.delete()
        return redirect("home")
    else:
        return redirect("index")


def delete_answer(request, id):
    if request.user.is_authenticated:
        answer = answer.objects.filter(id=id).first()
        answer.delete()
        return redirect("home")
    else:
        return redirect("index")


def delete_document(request, id):
    if request.user.is_authenticated:
        document = document.objects.filter(id=id).first()
        document.delete()
        return redirect("home")
    else:
        return redirect("index")


def delete_post(request, id):
    if request.user.is_authenticated:
        post = post.objects.filter(id=id).first()
        post.delete()
        return redirect("home")
    else:
        return redirect("index")


def delete_comment_Post(request, id):
    if request.user.is_authenticated:
        comment = comment_post.objects.filter(id=id).first()
        comment.delete()
        return redirect("home")
    else:
        return redirect("index")


def delete_comment_document(request, id):
    if request.user.is_authenticated:
        comment = comment_document.objects.filter(id=id).first()
        comment.delete()
        return redirect("home")
    else:
        return redirect("index")


def delete_payment_method(request, id):
    if request.user.is_authenticated:
        payment_method = payment_method.objects.filter(id=id).first()
        payment_method.delete()
        return redirect("home")
    else:
        return redirect("index")


def delete_trade(request, id):
    if request.user.is_authenticated:
        trade = trade.objects.filter(id=id).first()
        trade.delete()
        return redirect("home")
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
            document = Document.objects.filter(user=bio).last()
            post = Post.objects.filter(user=bio).last()
            question = Question.objects.filter(user=bio).last()
            gig = Gigs.objects.filter(user=bio).last()

            teen = float(web3.to_wei(
                contract.functions.balanceOf(your_bio.address).call(), 'ether'))

            context = {'user': bio, 'document': document,
                       'post': post, 'question': question, 'gig': gig, 'teen': teen}
    else:
        return redirect("index")
    return render(request, "user/user_profile.html", context)


def your_profile(request):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()

        # balanced
        eth_balanced = float(web3.to_wei(
            web3.eth.get_balance(bio.address), 'wei') / 1000000000000000000)
        teen_balanced = float(web3.to_wei(
            contract.functions.balanceOf(bio.address).call(), 'wei') / 1000000000000000000)

        # other
        document = Document.objects.filter(user=bio).last()
        post = Post.objects.filter(user=bio).last()
        question = Question.objects.filter(user=bio).last()
        gig = Gigs.objects.filter(user=bio).last()

        context = {'user': bio, 'document': document, 'post': post,
                   'question': question, 'gig': gig, 'eth': eth_balanced, 'teen': teen_balanced}
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


def apply_learning(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        post = Gigs.objects.filter(id=id).first()
        if bio and post:
            sql = join_cls(gig=post, student=bio)
            sql.save()
    else:
        return redirect('a_login')


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("index")
    else:
        return redirect("index")

# error


def all_error(request):
    return render(request, "error/all_error.html")

# tutor_function


def generate_payment(request, id, user_id):
    if request.user.is_authenticated:
        bio = Bio.objects.get(user=request.user)
        gig = Gigs.objects.get(id=id)
        if bio.user.id == gig.user.user.id:
            student = Bio.objects.filter(id=user_id).first()

            cls = join_cls.objects.filter(
                student=student, gig=gig, Status="Đang Học").first()
            learner = Learn.objects.filter(check_stu=cls).last()
            if cls:
                generate_link = "http://localhost:8000/payment/gig/" + \
                    str(cls.id)
                if not learner:
                    sql = Learn(check_stu=cls, cls_day=1)
                    sql.save()
                else:
                    sql = Learn(check_stu=cls, cls_day=learner.cls_day + 1)
                    sql.save()
                sql = gig_payment_link(link=generate_link)
                sql.save()
                sql = gig_payment_link.objects.filter(
                    link=generate_link).first()
                return redirect('copy_gig_payment_link', id=sql.id)
            else:
                return redirect("all_error")
    else:
        return redirect("index")


def copy_gig_payment_link(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.get(user=request.user)
        link = gig_payment_link.objects.get(id=id)
        if bio and link:
            teen_balanced = float(web3.to_wei(
                contract.functions.balanceOf(bio.address).call(), 'ether'))
            context = {'link': link, "teen": teen_balanced}
        else:
            return redirect("all_error")
    else:
        return redirect("index")
    return render(request, 'gigs/copy_payment_link.html', context)


def apply_to_gig(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.get(user=request.user)
        post = Gigs.objects.filter(id=id).first()
        check = join_cls.objects.get(gig=post, student=bio)
        if not check and bio != post.user:
            if check.Status != "Đang Học":
                sql = join_cls(gig=post, student=bio,
                               Status="Chờ Duyệt Đơn Đăng Ký")
                sql.save()
            else:
                return redirect("all_error")
            return redirect("gigs_view", id=id)
        else:
            return redirect("all_error")
    else:
        return redirect("index")


def accept_to_gig(request, id, user_id):
    if request.user.is_authenticated:
        bio = Bio.objects.get(user=request.user)
        student = Bio.objects.filter(user__id=user_id).first()
        post = Gigs.objects.filter(id=id).first()
        check = join_cls.objects.get(gig=post, student=student)
        if check and bio == post.user and student != post.user:
            check.Status = "Đang Học"
            check.save()
            return redirect("gigs_view", id=id)
        else:
            return redirect("all_error")
    else:
        return redirect("index")


def stop_learn_gig(request, id, user_id):
    if request.user.is_authenticated:
        bio = Bio.objects.get(user=request.user)
        student = Bio.objects.filter(user__id=user_id).first()
        post = Gigs.objects.filter(id=id).first()
        check = join_cls.objects.get(gig=post, student=student)
        if check and bio == post.user and student != post.user:
            if check.Status == "Đang Học":
                check.Status = "Dừng/Nghỉ/Hoàn Thành Học"
                check.save()
            else:
                return redirect("all_error")
            return redirect("gigs_view", id=id)
        else:
            return redirect("all_error")
    else:
        return redirect("index")


def check_apply(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.get(user=request.user)
        post = Gigs.objects.filter(id=id).first()
        check = join_cls.objects.filter(
            gig=post, Status="Chờ Duyệt Đơn Đăng Ký").all()
        if check and bio and post:
            context = {'students': check, 'gig': post}
        else:
            return redirect("all_error")
    else:
        return redirect("index")
    return render(request, "gigs/check_list.html", context)


def check_student(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.get(user=request.user)
        post = Gigs.objects.filter(id=id).first()
        check = join_cls.objects.filter(
            gig=post, Status="Đang Học").all()
        if check and bio and post:
            context = {'students': check, 'gig': post}
        else:
            return redirect("all_error")
    else:
        return redirect("index")
    return render(request, "gigs/check_list.html", context)


def view_all_gig(request):
    if request.user.is_authenticated:
        bio = Bio.objects.get(user=request.user)
        post = Gigs.objects.filter(user=bio).all()
        if bio and post:
            teen = float(Web3.to_wei(
                contract.functions.balanceOf(bio.address).call(), 'ether'))

            context = {'posts': post, 'teen': teen}
        else:
            return redirect("all_error")
    else:
        return render("a_login")
    return render(request, 'gigs/list.html', context)


def payment_bill(request, id):
    if request.user.is_authenticated:
        bio = Bio.objects.filter(user=request.user).first()
        check = join_cls.objects.filter(id=id).first()
        if bio and check:
            if bio == check.student and bio != check.gig.user:
                teen = float(Web3.to_wei(
                    contract.functions.balanceOf(bio.address).call(), 'ether'))

                context = {"info": check, 'teen': teen}
            else:
                return redirect("all_error")
        else:
            return redirect("all_error")
    else:
        return redirect("index")
    return render(request, "gigs/bill.html", context)
