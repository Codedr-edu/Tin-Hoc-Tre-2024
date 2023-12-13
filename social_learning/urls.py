from django.urls import path
from . import views

urlpatterns = [
    # index
    path('', views.index, name="index"),
    # authenticate
    path('accounts/login', views.Login, name="a_login"),
    path('accounts/sign/up/', views.Signup, name="signup"),
    path('logout/', views.log_out, name="log_out"),
    # like
    path('like/gig/<int:id>', views.like_gig, name="like_gig"),
    path('like/document/<int:id>', views.like_document, name="like_document"),
    path('like/post/<int:id>', views.like_post, name="like_post"),
    path('like/question/<int:id>', views.like_question, name="like_question"),
    path('like/answer/<int:id>', views.like_answer, name="like_answer"),
    # dislike
    path('dislike/gig/<int:id>', views.dislike_gig, name="dislike_gig"),
    path('dislike/document/<int:id>',
         views.dislike_document, name="dislike_document"),
    path('dislike/post/<int:id>', views.dislike_post, name="dislike_post"),
    path('dislike/question/<int:id>',
         views.dislike_question, name="dislike_question"),
    path('dislike/answer/<int:id>', views.dislike_answer, name="dislike_answer"),
    # answer
    path('answer/question/<int:id>', views.answer, name="answer"),
    # comment
    path('comment/post/<int:id>', views.comment_post, name="comment_post"),
    path('comment/document/<int:id>',
         views.comment_document, name="comment_document"),
    path('comment/gig/<int:id>',
         views.comment_gig, name="comment_gig"),
    # reply_comment
    path('reply/comment/post/<int:id>',
         views.reply_comment_post, name="reply_comment_post"),
    path('reply/comment/document/<int:id>',
         views.reply_comment_document, name="reply_comment_document"),
    path('reply/comment/gig/<int:id>',
         views.reply_comment_gig, name="reply_comment_gig"),
    # read
    path("view/comment/post/<int:id>",
         views.comment_post_view, name="comment_post_view"),
    path("view/document/<int:id>", views.document_view, name="document_view"),
    path("view/question/<int:id>",
         views.question_view, name="question_view"),
    path("view/gig/<int:id>", views.gigs_view, name="gigs_view"),
    # create
    path("create/post/", views.post_create, name="create_post"),
    path("create/document/", views.document_create, name="create_document"),
    path("create/gig/", views.gigs_create, name="create_gigs"),
    path("create/question/", views.question_create, name="create_question"),
    path('create/trade/', views.create_trade_offer, name="create_trade"),
    # update
    path("update/post/<int:id>", views.update_post, name="update_post"),
    path("update/document/<int:id>", views.update_document, name="update_document"),
    path("update/gig/<int:id>", views.update_gig, name="update_gig"),
    path("update/question/<int:id>", views.update_question, name="update_question"),
    path("update/answer/<int:id>", views.update_answer, name="update_anwer"),
    path("update/comment/post/<int:id>",
         views.update_comment_post, name="update_comment_post"),
    path("update/comment/document/<int:id>",
         views.update_comment_document, name="update_comment_document"),
    path("update/comment/gig/<int:id>",
         views.update_comment_gigs, name="update_comment_gig"),
    # delete
    path("delete/post/<int:id>", views.delete_post, name="delete_post"),
    path("delete/document/<int:id>", views.delete_document, name="delete_document"),
    path("delete/gig/<int:id>", views.delete_gigs, name="delete_gig"),
    path("delete/question/<int:id>", views.delete_question, name="delete_question"),
    path("delete/answer/<int:id>", views.delete_answer, name="delete_answer"),
    path("delete/comment/post/<int:id>",
         views.delete_comment_Post, name="delete_comment_post"),
    path("delete/comment/document/<int:id>",
         views.delete_comment_document, name="delete_comment_document"),
    path("delete/comment/gig/<int:id>",
         views.delete_comment_gig, name="delete_comment_gig"),
    # user
    path("user/<int:id>", views.user_profile, name="user_profile"),
    path("your/profile/", views.your_profile, name="your_profile"),
    path("delete/profile/", views.delete_user, name="delete_profile"),
    path("add/social/media", views.add_social_media, name="add_social_media"),
    path("update/profile", views.update_profile, name="update_profile"),
    # search
    path("search/post/", views.search_post, name="search_post"),
    path("search/document/", views.search_document, name="search_document"),
    path("search/gig/", views.search_gig, name="search_gigs"),
    path("search/question/", views.search_question, name="search_post"),
    # search_result
    path("search/post?q=<q>", views.searched_post_list_view,
         name="search_result_post"),
    path("search/document?q=<q>", views.searched_document_list_view,
         name="search_result_document"),
    path("search/gig?q=<q>", views.searched_gigs_list_view,
         name="search_result_gigs"),
    path("search/question?q=<q>", views.searched_question_list_view,
         name="search_result_post"),
    # payment
    path("payment/question/<int:id>", views.question_payment, name="pay_question"),
    path("payment/document/<int:id>", views.document_payment, name="pay_document"),
    path("payment/gig/<int:id>",
         views.gigs_payment, name="pay_gig"),
    # trade
    path("trade/eth/to/teen/<int:id>",
         views.eth_to_teen, name="trade_eth_to_teen"),
    path("trade/teen/to/eth/<int:id>",
         views.teen_to_eth, name="trade_teen_to_eth"),
    # transfer
    path("transfer/teen/", views.teen_transfer, name="teen_transfer"),
    path("transfer/eth/", views.eth_transfer, name="eth_transfer"),
    # list_view
    path("post/",
         views.post_list_view, name="post"),
    path("document/", views.document_list_view, name="document"),
    path("question/",
         views.question_list_view, name="question"),
    path("gig/", views.gigs_list_view, name="gigs"),
    path("trade/", views.trade_list_view, name="trade"),
    # all_error
    path("error/all/", views.all_error, name="all_error"),
    # gig_payment_link
    path("generate/payment/link/gig/<int:id>/user/<int:user_id>",
         views.generate_payment, name="generation_link_payment"),
    path("copy/gig/payment/link/<int:id>",
         views.copy_gig_payment_link, name="copy_gig_payment_link"),
    # gig_other_view_function
    path("gigs/user/all/", views.view_all_gig, name="user_gigs_view_all"),
    path("apply/list/gig/<int:id>", views.check_apply, name="apply_list_check"),
    path("student/list/gig/<int:id>",
         views.check_student, name="student_apply_gig"),
    # gig_other_function
    path("apply/gig/<int:id>", views.apply_to_gig, name="apply_gig"),
    path("accept/gig/<int:id>/user/<int:user_id>",
         views.accept_to_gig, name="accept_gig"),
    path("stop/gig/<int:id>/user/<int:user_id>",
         views.stop_learn_gig, name="stop_learn_gig"),
    path("check/", views.check, name="check"),
    path("payment/bill/<int:id>", views.payment_bill, name="payment_bill")
]
