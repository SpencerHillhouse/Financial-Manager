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
    # path('create_profile/', views.create_profile, name="create_profile"),
    path('delete_user/<str:pk>/', views.delete_user, name="delete_user"),
    path('create_account/', views.create_account, name="create_account"),
]