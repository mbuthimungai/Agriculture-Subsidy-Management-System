from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login-view'),
    path('signup', views.sign_up, name='Sign up view'),
    path('token-test', views.token_test, name="Token test view")
]
