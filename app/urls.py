from django.urls import path
from .views import *

urlpatterns = [

    path('',index,name="index-page"),
    path('signup/',signup,name="signup-page"),
    path('subscriptions/',SubscriptionPage,name="subscription-page"),
    path('subscriptions-details/',SubscriptionDetails,name="subscriptiondetails-page")
]



