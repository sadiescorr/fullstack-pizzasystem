from django.urls import path
from . import views
from .forms import *

urlpatterns = [
   path('base/', views.base, name="base"),
   path('user_signup/', views.UserSignupView.as_view(), name="user_signup"),
   path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm)),
   path('logout/', views.logout_user, name="logout"),
   path('account/', views.account, name="account"),
   path('', views.home, name="home"),
   path('orderhistory/', views.orderhistory, name="orderhistory"),
   path('createorder/', views.createorder, name="createorder"),
   path('payment/', views.payment, name="payment"),
   path('order_summary/', views.order_summary, name="order_summary"),
]