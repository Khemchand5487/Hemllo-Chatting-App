from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('register2', views.otp_verification, name="register2"),
    path("login/forgot_password", views.forgot_password, name='forgot_password'),
    path("login/forgot_password/send_otp_mail", views.send_reset_mail, name='forgot_password/send_otp_mail'),
    path("login/forgot_password/verify_reset_otp", views.verify_reset_otp, name='forgot_password/verify_reset_otp'),
    path("login/forgot_password/reset", views.change_pwd, name='forgot_password/reset'),
    path("main", views.main_app, name="main")
]
