from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

from rest_framework import serializers

class Customer(models.Model):

    Genders = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    customer_gender = models.CharField(null=True, choices=Genders, max_length=10)
    region = models.CharField(max_length=50, null=True)


class Policy(models.Model):

    Marital_Status = (
        ('1', 'Married'),
        ('0', 'Unmarried')
    )
    policy_id = models.IntegerField(unique=True,null=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    date_of_purchase = models.DateField(max_length=100,null=True, blank=True)
    fuel = models.CharField(max_length=20, null=True)
    vehicle_segment = models.CharField(max_length=2, null=True)
    premium = models.IntegerField(null=True)
    injury_liability = models.IntegerField(default=0)
    injury_protection = models.IntegerField(default=0)
    damage_liability = models.IntegerField(default=0)
    collision = models.IntegerField(default=0)
    comprehensive = models.IntegerField(default=0)
    income = models.CharField(max_length=100, null=True)
    marital_status = models.IntegerField(choices=Marital_Status, default=0, null=True)

    def save(self, *args, **kwargs):
        if self.premium > 1000000:
            raise serializers.ValidationError('Premium should not be allowed more than 1 million')
        super(Policy, self).save(*args, **kwargs)