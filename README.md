# cabin

Cabin 2

# description

It all started with Uber. A great idea that connects
drivers to passengers and anyone anywhere can quickly
request a taxi for themselves.
It wasn't long before our dear domestic
programmers got an idea from this service and started to
implement it in Iran. Currently, there are several online
taxi request services that are serving passengers in Tehran
and several other cities, and they are expanding day by day
and have created many jobs. Now, due to the hot market of this
service, we also want to create a similar service. We have also named it cabin.

# structure of django project

    ├─── manage.py

    ├─── requirements.txt
    │

    ├─── cabin
    │ ├─── admin.py
    │ ├─── apps.py
    │ ├─── models.py
    │ ├─── > queries.py <  We should write Optimized queries >
    │ ├─── views.py
    │ ├─── init.py
    │ │
    │ ├─── fixtures
    │ │ └─── sample_test_fixture.json
    │ │
    │ └─── migrations
    │   ├── 0001_initial.py
    │   └─── init.py
    │
    ├───challenge
    │ ├─── settings.py
    │ ├─── urls.py
    │ ├─── wsgi.py
    │ └─── init.py
    │
    └───tests
        ├─── testsample.py
        └─── init.py

# initialization

install python3 and add new virtualenv

install packages with pip3 install -r requirements.txt

python manage.py migrate

python manage.py loaddata cabin/fixtures/sample_test_fixture.json

python mange.py runserver 8080

# test all test cases

python manage.py test

# for test specific queries

python manage.py test tests.testsample.SampleTests.test_1

# queries problems

queries.py file

    1. The total amount received by a driver with an ID equal to x.
    2. The list of all trips by a passenger with ID x.
    3. The number of trips that had a duration (in terms of time) greater than t.
    4. The list of all drivers who are within a distance less than or equal 
        to r around the point (x, y) and are also active (ready for work).
    5. The list of drivers who have either a class A car or a car with color c
        and have completed at least n trips.
    6. The list of passengers who have had x or more trips and 
        have paid more than t in total.
    7. The list of drivers who have had at least one trip in which the driver's name matches the passenger's name.
    8. The list of all drivers with an additional column named "n," 
        indicating the number of trips in which the driver's last name matches the passenger's last name.
    9. The list of all drivers along with an additional column named "n," 
        which represents the number of trips in which the car model was X or
        higher (note that the model is different from the type) and the trip duration was more than t seconds.
    10. The list of all cars with an additional column named "extra."


