from django.db.models import Subquery, OuterRef, Sum, When, Case, IntegerField, F, Value, Q, Count, FloatField, \
    ExpressionWrapper, DurationField
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
    # this is only help for model relations

    # level1: Rider
    # level2: RideRequest
    # level3: Ride
    # level4: Payment

    # Subquery to calculate the ride request count of each rider (that equals to ride count)
    ride_count_subquery = Ride.objects.filter(
        request__rider=OuterRef('pk')
    ).values('request__rider').annotate(
        ride_count=Count('id')
    ).values('ride_count')

    # Subquery to calculate the total payment amount for each rider
    total_payment_subquery = Ride.objects.filter(
        request__rider=OuterRef('pk')
    ).values('request__rider').annotate(
        total_payment=Sum('payment__amount')
    ).values('total_payment')

    # Query to filter riders who meet the criteria
    riders_queryset = Rider.objects.annotate(
        ride_count=Subquery(ride_count_subquery, output_field=models.IntegerField()),
        total_payment=Subquery(total_payment_subquery, output_field=models.FloatField())
    ).filter(
        Q(ride_count__gte=x) & Q(total_payment__gt=t)
    )
    return riders_queryset


def query_7():
    # find drivers with 1 or more than ride_request that has same first_name with the rider

    # Annotate the number of ride requests with the same first_name as the driver's
    drivers_with_request_count = Driver.objects.annotate(
        request_count=Count(
            expression='car__ride__request',
            filter=Q(car__ride__request__rider__account__first_name=F('account__first_name'))
        )
    )

    # Filter drivers with 1 or more ride requests that have the same first_name
    q = drivers_with_request_count.filter(request_count__gte=1)
    return q


def query_8():
    q = Driver.objects.annotate(
        n=Count(
            expression='car__ride__request',
            filter=Q(car__ride__request__rider__account__last_name=F('account__last_name'))
        )
    )
    return q


def query_9(x, t):

    # find all Drivers rides counts that have greater than or eqaul x
    # model driver Car and also dropp_off_time - pickup_time >= t
    q = Driver.objects.annotate(
        n=Count('car__ride',
                filter=Q(car__model__gte=x) & Q(car__ride__dropoff_time__gte=F('car__ride__pickup_time') + t),
                distinct=True
                ),
    ).values('id', 'n')
    return q


def query_10():
    # way 1
    # rides_subquery = Ride.objects.filter(
    #     car=OuterRef('pk')
    # ).annotate(
    #     ride_count=Count('id', distinct=True),
    #     ride_length=F('dropoff_time') - F('pickup_time'),
    #     payment_sum=Sum('payment__amount', distinct=True)
    # )
    #
    # q = Car.objects.annotate(
    #     extra=Case(
    #         When(
    #             car_type='A', then=Coalesce(
    #                 Subquery(
    #                     rides_subquery.values('ride_count')
    #                 ),
    #                 Value(0),
    #                 output_field=IntegerField()
    #             )
    #         ),
    #         When(
    #             car_type='B', then=Coalesce(
    #                 Subquery(
    #                     rides_subquery.values('ride_length')
    #                 ),
    #                 Value(0),
    #                 output_field=IntegerField()
    #             )
    #         ),
    #         When(
    #             car_type='C', then=Coalesce(
    #                 Subquery(
    #                     rides_subquery.values('payment_sum')
    #                 ),
    #                 Value(0),
    #                 output_field=IntegerField()
    #             )
    #         ),
    #         output_field=IntegerField()
    #     )
    # ).distinct()
    # print([i.extra for i in q])

    # way 2
    # car_extra_subquery = Car.objects.filter(pk=OuterRef('pk')).annotate(
    #     extra=Case(
    #         When(car_type='A', then=Count('ride', distinct=True)),
    #         When(car_type='B', then=Sum(F('ride__dropoff_time') - F('ride__pickup_time'), default=Value(0))),
    #         When(car_type='C', then=Sum(F('ride__payment__amount'), default=Value(0))),
    #         default=Value(0),
    #         output_field=IntegerField()
    #     )
    # ).values('extra')
    #
    # cars_with_extra = Car.objects.annotate(
    #     extra=Subquery(car_extra_subquery, output_field=IntegerField())
    # )
    # print([i.extra for i in cars_with_extra])
    # return cars_with_extra

    # rides_subquery = Ride.objects.filter(
    #     car=OuterRef('pk')
    # ).annotate(
    #     ride_length=F('dropoff_time') - F('pickup_time'),
    # ).values('ride_length').annotate(ride_duration=Sum('ride_length')).values('ride_duration')
    #
    #
    # rides_subquery2 = Ride.objects.filter(
    #     car=OuterRef('pk')
    # ).values('payment__amount').annotate(payment_sum=Sum('payment__amount')).values('payment_sum')



    # way 3
    # q = Car.objects.annotate(
    #     extra=Case(
    #         When(
    #             car_type='A', then=Count('ride', distinct=True)
    #         ),
    #         When(
    #             car_type='B', then=Sum((F('ride__dropoff_time') - F('ride__pickup_time')), default=Value(0))
    #         ),
    #         When(
    #             car_type='C', then=Sum('ride__payment__amount', default=Value(0))
    #         ),
    #         default=Value(0),
    #         output_field=IntegerField()
    #     )
    # )

    # way 4
    # ride_duration_subquery = Ride.objects.filter(car=OuterRef('pk')).annotate(
    #     duration=ExpressionWrapper(
    #         F('dropoff_time') - F('pickup_time'),
    #         output_field=IntegerField()
    #     )
    # ).values('car__pk').annotate(
    #     total_duration=Sum('duration')
    # ).values('total_duration')
    #
    # ride_costs_subquery = Ride.objects.filter(car=OuterRef('pk')).annotate(
    #     total_ride_cost=Sum(F('payment__amount'))
    # ).values('total_ride_cost')
    #
    # cars_with_extra = Car.objects.annotate(
    #     extra=Case(
    #         When(car_type='A', then=Count('ride', distinct=True)),
    #         When(car_type='B', then=Subquery(ride_duration_subquery, output_field=DurationField())),
    #         When(car_type='C', then=Subquery(ride_costs_subquery, output_field=FloatField())),
    #         default=Value(0),
    #         output_field=FloatField()  # Set the default output field to FloatField
    #     )
    # )
    # print(cars_with_extra)

    # return q
    pass