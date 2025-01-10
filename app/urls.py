from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name ="logout"),
    path('register/', views.registerPage, name="register"),
    path('transactions/', views.transactionPage, name="transaction-page"),
    path('create_transaction/', views.create_transaction, name='create_transaction'),
]