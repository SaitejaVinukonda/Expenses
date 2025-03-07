from django.db import models

# Create your models here.
class currentbalance(models.Model):
    current_balance=models.FloatField(default=0)
class TrackingHistory(models.Model):
    current_balance=models.ForeignKey(currentbalance,on_delete=models.CASCADE)
    amount=models.FloatField()
    expense_type=models.CharField(choices=(('credit','credit'),('debit','debit')),max_length=200)
    description=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now=True)