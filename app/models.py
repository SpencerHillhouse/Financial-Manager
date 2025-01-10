from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=200, null=True)
    date_create = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class SavingsAccount(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return self.user.name
    
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    )

    profileuser = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    # balance = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=10)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.description
    
def create_profile( name, phone, email):
    profile_to_create = Profile(name=name, phone=phone, email=email)
    profile_to_create.save()
    return profile_to_create

def creaet_savings_account(user, balance):
    if not user:
        raise ValueError
    else:
        savings_account_to_create = SavingsAccount(user=user, balance=balance)
        savings_account_to_create.save()
        return savings_account_to_create
    

def create_transaction(profileuser, amount, transaction_type, description):
    
    if not profileuser:
        raise ValueError
    else:
        transaction_to_create = Transaction(profileuser=profileuser, amount=amount, transaction_type = transaction_type, description=description)
        account_to_get = SavingsAccount.objects.get(user=profileuser)
        if transaction_to_create.transaction_type == 'withdraw':
            account_to_get.balance = account_to_get.balance - transaction_to_create.amount
        else:
            account_to_get.balance += transaction_to_create.amount
        account_to_get.save()
        print(f"Balance: {account_to_get.balance}")
        transaction_to_create.save()
        return transaction_to_create
    