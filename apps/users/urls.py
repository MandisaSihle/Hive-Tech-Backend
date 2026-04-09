from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserSignUp.as_view(), name='user_sign_up'),
    path('signin/', views.UserSignIn.as_view(), name='user_sign_in'),
    path('profile/', views.UserProfile.as_view(), name='user_profile'),
]