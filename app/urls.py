from django.urls import path
from .views import *

urlpatterns = [

    path('',index,name="index-page"),
    path('signup/',signup,name="signup-page"),
    path('login/',login,name="login-page"),
    # path('subscriptions/',SubscriptionPage,name="subscription-page"),
    path('logout/',Logout,name="logout-function"),
    path('subscriptions/car-details/<int:id>/',Details,name="subscription-details"),
    path('guide/',Guide,name="guide-content"),
    path('contact/',contact,name="contact-page"),
    path('blog-news/',blog,name="blog-page"),
    path('add-comment/<int:pk>/',add_comment,name="addblog-page"),
    path('FAQ/',FAQ_Function,name="faq-page"),
    path('schedule/',schedule_appointment,name="scheduling-page"),
    path('profile/',Profile,name="profile-page"),
    path('subscribe/',Subscribe,name="subscription-details-page"),
    path('success/',Success,name="success-page"),
    path('error/',Error,name="error-page"),
    path('admin-login/',AdminLogin,name="adminlogin-page"),
    # Dashboard urls
    path('dashboard/',Dashboard,name="Dashboard-Page"),
    path('addblog/',Addblog,name="addblog-Page"),
    path('addblog-success/',adminsuccess,name="addblogsuccess-Page"),
    path('appointments/',Appointments,name="appoinetments-Page")

]
