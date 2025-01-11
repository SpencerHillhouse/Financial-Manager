from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from .models import *
from .forms import *
from .decorators import unathenticated_user, allowed_users, admin_only

# Create your views here.


@login_required(login_url='login')
@admin_only
def home(request):
    profile = User.objects.all()
    account = SavingsAccount.objects.all()
    return render(request, 'accounts/dashboard.html', {'profile':profile, 'account':account})

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['accountholder'])
# def create_profile(request):
#     form = NewUserForm()
#     if request.method =="POST":
#         form = NewUserForm(request.POST)
#         if form.is_valid:
#             new_profile = form.save()
#             return form
#     context={'form': form}
#     return render(request, 'accounts/new_profile_form.html', context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['accountholder'])
def userPage(request):
    profile = Profile.objects.all()
    print(profile)
    account = SavingsAccount.objects.all()
    content = {}
    return render(request, 'accounts/user.html', {'profile':profile, 'account':account})


@login_required(login_url='login')
# @allowed_users(allowed_roles=['accountholder'])
def transactionPage(request):
    transactions = request.user.profile.transaction_set.all()
    account = request.user.profile.savingsaccount_set.all()
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
            target_user = User.objects.get(username=username)
            new_profile = Profile(user=target_user)
            new_profile.save()
            group = Group.objects.get(name='accountholder')
            user.groups.add(group)
            messages.success(request, 'Account was created for ' + username)
            
            return redirect('login')
    context = {'form' :form}
    return render(request, 'accounts/register.html', context)



@login_required(login_url='login')
def create_transaction(request):
    form = CreateTransactionForm()
    if request.method == 'POST':
        form = CreateTransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            transaction_type = form.cleaned_data.get('transaction_type')
            description = form.cleaned_data.get('description')
            target_user = User.objects.get(pk=request.POST.get("user_profile_id"))
            for a in SavingsAccount.objects.all():
                if target_user == a.user.user:
                    if transaction_type == 'deposit':  
                        # add to balance
                        a.balance += amount
                        a.save()
                        new_transaction = Transaction(profileuser=target_user.profile,amount=amount, transaction_type=transaction_type, description=description, balance=a.balance)  
                        new_transaction.save()
                    else:
                        a.balance -= amount
                        a.save()
                        new_transaction = Transaction(profileuser=target_user.profile,amount=amount, transaction_type=transaction_type, description=description, balance=a.balance) 
                        new_transaction.save()
            return redirect('home')
    context={'form': form}
    return render(request, 'accounts/create_transaction_form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_user(request,pk):
    profile = Profile.objects.get(id=pk)
    print(profile)
    user = User.objects.get(id=pk)
    print(user)
    context = {'profile':profile}
    if profile.user == user:
        return render(request, 'accounts/delete_user.html', context)
    else:
        print("It broke but it shouldn't have help")
        
    # return redirect('home')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def remove_user(request,pk):
    user = User.objects.get(id=pk)
    user.delete()    
    return redirect('home')

@login_required(login_url='login')
@allowed_users(allowed_roles=['accountholder'])
def create_account(request):
    form = NewAccountForm()
    if request.method == "POST":
        form = NewAccountForm(request.POST)
        if form.is_valid():
            balance = form.cleaned_data.get('balance')
            target_user_profile = User.objects.get(pk=request.POST.get("user_profile_id")).profile
            new_account = SavingsAccount(user=target_user_profile, balance=balance)
            new_account.save()
            return redirect('user-page')
    context = {'form':form}
    return render(request, 'accounts/new_account.html', context)