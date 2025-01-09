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

# class SavingsAccount(models.Model):
#     balance = models.DecimalField(max_digits=12, decimal_places=2)
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.name
    
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
    

    
# def create_transaction(user, amount, transaction_type, description):
#     user = Transaction.objects.get(user=user)
#     transaction_to_create = Transaction(user=user, amount=amount, transaction_type = transaction_type, description=description)
#     if transaction_to_create.transaction_type == 'withdraw':
#         transaction_to_create.balance -= transaction_to_create.amount
#     else:
#         transaction_to_create.balance += transaction_to_create.amount
#     transaction_to_create.save()
#     return transaction_to_create