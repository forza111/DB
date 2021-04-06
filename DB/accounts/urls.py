from django.contrib.auth import views as authviews
from . import views
from django.urls import path

urlpatterns = [
    path('login/', authviews.LoginView.as_view(), name='login'),
    path('logout/', authviews.LogoutView.as_view(), name='logout'),
    path('', views.ScoreView.as_view(), name='score')
]