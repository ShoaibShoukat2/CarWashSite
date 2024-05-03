from django.urls import path
from .views import *

urlpatterns = [

    path('',index,name="index-page"),
    path('signup/',signup,name="signup-page"),
    path('login/',login,name="login-page"),
    path('subscriptions/',SubscriptionPage,name="subscription-page"),
    path('logout/',Logout,name="logout-function"),
    path('subscriptions/car-details/<int:id>/',Details,name="subscription-details"),
    path('guide/',Guide,name="guide-content"),
    path('contact/',contact,name="contact-page"),
    path('blog-news/',blog,name="blog-page"),
    path('add-comment/<int:pk>/',add_comment,name="addblog-page"),
    path('FAQ/',FAQ_Function,name="faq-page"),
    path('schedule/',Schedule,name="scheduling-page")
]



