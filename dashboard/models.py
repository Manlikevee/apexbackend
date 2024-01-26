from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Accountdetails(models.Model):
    requestuser = models.OneToOneField(User, on_delete=models.CASCADE)
    bank_code = models.CharField(blank=True, max_length=500, default='02928')
    bank_name = models.CharField(blank=True, max_length=500, default='pwb Financial Bank')
    account_number = models.CharField(default=234, blank=True, max_length=500)
    account_name = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.account_number

class Userstatus(models.Model):
    Workstatus = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(blank=True, max_length=500, choices=Workstatus, default='Inactive')


    def __str__(self):
        return self.status

class Transaction(models.Model):
    Workstatus = [
        ('pending confirmation', 'pending confirmation'),
        ('submitted for review', 'submitted for review'),
        ('Awaiting Payment', 'Awaiting Payment'),
        ('confirmed', 'confirmed'),
        ('cancelled', 'cancelled'),
    ]

    creditordebit = [
        ('credit', 'credit'),
        ('debit', 'debit'),
    ]

    reference = models.CharField(blank=True, max_length=500)
    requestuser = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, blank=True, choices=creditordebit)
    status = models.CharField(blank=True, max_length=500, choices=Workstatus, default='pending confirmation')
    witholdingtax  = models.DecimalField(blank=True, decimal_places=2, max_digits=60, default=0)
    amount = models.FloatField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    narration = models.CharField(blank=True, null=True, max_length=500)
    payment_data = models.JSONField(blank=True, null=True)
    bankdetails = models.JSONField(blank=True, null=True)
    paymentto = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.status


class Support(models.Model):
    Accounttype = [
        ('transfer', 'transfer'),
        ('userdata', 'userdata'),
        ('passwordreset', 'passwordreset'),

    ]

    Workstatus = [
        ('pending', 'pending'),
        ('Resolved', 'Resolved'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reference = models.CharField(blank=True, max_length=500)
    title = models.CharField(blank=True, max_length=500)
    description = models.TextField(blank=True, max_length=5000)
    affected_area = models.CharField(max_length=100, default='pending', choices=Accounttype)
    status = models.CharField(blank=True, max_length=500, choices=Workstatus, default='pending')
    posteddate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Beneficiary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accountname = models.CharField(blank=True, max_length=500)
    accountnumber = models.CharField(blank=True, max_length=500)
    bankname = models.TextField(blank=True, max_length=5000)
    posteddate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.accountname



class contactus(models.Model):
    name = models.CharField(blank=True, max_length=500)
    reason = models.CharField(blank=True, max_length=500)
    reference = models.CharField(blank=True, max_length=500)
    email = models.EmailField(blank=True, max_length=500)
    phonenumber = models.CharField(blank=True, max_length=500)
    message = models.TextField(blank=True, max_length=5000)
    posteddate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class latestupdate(models.Model):
    Workstatus = [
        ('Withdrawal', 'Withdrawal'),
        ('Support', 'Support'),
        ('Deposit', 'Deposit'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.CharField(blank=True, max_length=500, choices=Workstatus, default='Inactive')
    text = models.CharField(blank=True, max_length=500)
    ref =  models.CharField(blank=True, max_length=500)

