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
    path('blog-news/',Blog,name="blog-page")
]



