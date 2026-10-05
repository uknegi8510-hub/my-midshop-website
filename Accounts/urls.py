from django.urls import include,path
from Products.views import *
from Accounts import views
from Accounts.views import*


urlpatterns = [
    path("login_page/",views.login_page,name="login_page"),
    path("logout_page/",views.logout_page,name="logout_page"),
]
