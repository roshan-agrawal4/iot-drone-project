from django.urls import path
from .  import views



urlpatterns = [
path('',views.index,name="drone"),
path('check-drone-status',views.check_drone_status,name="check-drone-status"),
path('home',views.home_page,name="home"),
path('login',views.login_page,name="login"),
path('signup',views.signup_page,name="signup"),
path('signout',views.sign_out,name="signout")
]
