from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user}"

class SavingsAccount(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.user.user.first_name}"
    
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    )

    profileuser = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=10)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return self.description
    
