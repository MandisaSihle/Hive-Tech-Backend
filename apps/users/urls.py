from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserSignUp.as_view(), name='user-signup'),
    path('signin/', views.UserSignIn.as_view(), name='user-signin'),
    path('profile/', views.UserProfile.as_view(), name='user-profile'),
]