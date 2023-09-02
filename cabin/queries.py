from django.db.models import Subquery, OuterRef, Sum, When, Case, IntegerField, F, Value, Q, Count, FloatField, \
    ExpressionWrapper
from django.db.models.functions import Coalesce, Abs, Sqrt

from cabin.models import *


def query_0(x):
    q = Driver.objects.filter(rating__gt=x)
    return q


def query_1(x):
    # this is only help for model relations
    # level1 :Payment (ride) ->
    # level2 :Ride (car) ->
    # level3 :Car (owner) ->
    # level4 :Driver

    # we should aggregate payments of the ride that have the exact car that belong to specific owner (driver)
    # we use objects aggregate with using Sum , When and Case django expressions to
    # find every driver ( we named it Conditional Sum)
    q = Payment.objects.aggregate(
        payment_sum=Sum(
            Case(
                When(
                    # we use id because of the foreign key is indexed on db and has better performance
                    # in comparsion to ride__car__owner ( this snippet need compare every objects)
                    # but the way compare indexed id and have better performance
                    ride__car__owner__id=x, then='amount'
                ),
                default=None,
                output_field=IntegerField()
            )
        )
    )
    return q


def query_2(x):
    q = 'your query here'
    return q


def query_3(t):
    q = 'your query here'
    return q


def query_4(x, y, r):
    q = 'your query here'
    return q


def query_5(n, c):
    q = 'your query here'
    return q


def query_6(x, t):
    q = 'your query here'
    return q


def query_7():
    q = 'your query here'
    return q


def query_8():
    q = 'your query here'
    return q


def query_9(n, t):
    q = 'your query here'
    return q


def query_10():
    q = 'your query here'
    return q