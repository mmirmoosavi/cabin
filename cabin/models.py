from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

car_type_choices = (
    ('A', 'class A'),
    ('B', 'class B'),
    ('C', 'class C'),
)


class Account(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, unique=True)
    phone = models.CharField(max_length=15, unique=True, primary_key=True)
    password = models.CharField(max_length=50)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None)
    object_id = models.PositiveIntegerField(default=None)
    content_object = GenericForeignKey()

    class Meta:
        unique_together = ('content_type', 'object_id',)


class Admin(models.Model):
    account = GenericRelation(Account, related_query_name='admins')


class Rider(models.Model):
    account = GenericRelation(Account, related_query_name='riders')
    rating = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()


class Driver(models.Model):
    account = GenericRelation(Account, related_query_name='drivers')
    rating = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    active = models.BooleanField(default=False)


class RideRequest(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    car_type = models.CharField(max_length=3, choices=car_type_choices)


class Car(models.Model):
    owner = models.ForeignKey(Driver, on_delete=models.CASCADE)
    car_type = models.CharField(max_length=3, choices=car_type_choices)
    model = models.IntegerField()
    color = models.CharField(max_length=10)


class Ride(models.Model):
    pickup_time = models.IntegerField()
    dropoff_time = models.IntegerField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    request = models.OneToOneField(RideRequest, on_delete=models.CASCADE, null=False)
    rider_rating = models.FloatField()
    driver_rating = models.FloatField()


class Payment(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.IntegerField()
    # any other payment data
