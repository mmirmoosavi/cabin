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
    # this is only help for model relations

    # level1: Ride (request) ->
    # level2: RideRequest (rider) ->
    # level3: Rider
    # finds all rides with driver_id = x
    q = Ride.objects.filter(request__rider__id=x)
    return q


def query_3(t):
    # annotate all ride time length to Ride Objects
    ride_with_t_length_queryset = Ride.objects.annotate(ride_time_length=F('dropoff_time') - F('pickup_time'))
    # count rides with more than t time length
    q = ride_with_t_length_queryset.filter(ride_time_length__gt=t).count()
    return q


def query_4(x, y, r):
    # filter only active drivers first
    act_driver_and_first_location_filter = Driver.objects.filter(
        active=True
    )
    # compute euclidean distance with annotation
    annotate_x2_y2_square = act_driver_and_first_location_filter.annotate(
        euclidean_distance=ExpressionWrapper(
            (
                (Sqrt((F('x') - x) ** 2 + (F('y') - y) ** 2))
            ),
            output_field=FloatField()
        )
    )
    final_queryset = annotate_x2_y2_square.filter(euclidean_distance__lte=r)

    return final_queryset


def query_5(n, c):
    # this is only help for model relations

    # level1: Ride (car) ->
    # level2: Car (owner) ->
    # level3: Driver

    # find divers that have >= n trip and have at least A car_type or c Color

    drivers_with_n_trips_and_car = Driver.objects.annotate(
        trip_count=Count('car__ride')
    ).filter(
        Q(trip_count__gte=n) &
        (Q(car__car_type='A') | Q(car__color=c))
    ).distinct()
    return drivers_with_n_trips_and_car


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