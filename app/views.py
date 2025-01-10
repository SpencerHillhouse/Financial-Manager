from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import *
from .decorators import unathenticated_user, allowed_users, admin_only

# Create your views here.


@login_required(login_url='login')
@admin_only
def home(request):
    profile = Profile.objects.all()
    account = SavingsAccount.objects.all()
    return render(request, 'accounts/dashboard.html', {'profile':profile, 'account':account})

@login_required(login_url='login')
@allowed_users(allowed_roles=['accountholder'])
def userPage(request):
    transactions = request.user.profile.transaction_set.all()
    print("Transactions:", transactions)
    content = {}
    return render(request, 'accounts/user.html')


@login_required(login_url='login')
# @allowed_users(allowed_roles=['accountholder'])
def transactionPage(request):
    # transactions = Transaction.objects.all()
    transactions = request.user.profile.transaction_set.all()
    account = request.user.profile.savingsaccount_set.all()
    # balance = account.objects.get.all()
    print("Transactions: ", transactions)
    print("Account: ", account)
    # print("Balance: ", balance)
    
    return render(request, 'accounts/transactions.html', {'transactions':transactions, 'account':account}) 


@unathenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or Password is incorrect")

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@unathenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='accountholder')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
    context = {'form' :form}
    return render(request, 'accounts/register.html', context)

def create_transaction(request):
    form = CreateTransactionForm()
    if request.method == 'POST':
        print('Printing POST:', request.POST)
        
    context={'form': form}
    return render(request, 'accounts/create_transaction_form.html', context)