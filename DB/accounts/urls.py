from django.contrib.auth import views as authviews
from . import views
from django.urls import path


urlpatterns = [
    path('login/', authviews.LoginView.as_view(), name='login'),
    path('logout/', authviews.LogoutView.as_view(), name='logout'),

    path('', views.index, name='main'),
    path('personal_account/', views.UserDetail.as_view(), name='personal_cabinet'),
    path('payment_schedule/<int:pk>', views.PaymentsShedule.as_view(), name='payment_schedule')

]