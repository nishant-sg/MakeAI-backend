from django.contrib import admin
from django.urls import path,include
from .views import RegisterView,LoginView,UserView,LogoutView,ClearDatabaseView,ActivateView,RequestResetPasswordView,ResetPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('users/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('clearData/', ClearDatabaseView.as_view()),
    path('activate/<uidb64>/<token>', ActivateView.as_view(),name='activate'),
    path('requestresetpassword/', RequestResetPasswordView.as_view()),
    path('reset/<uidb64>/<token>', ResetPasswordView.as_view(),name='reset'),
]
