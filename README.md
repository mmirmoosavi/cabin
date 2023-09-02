# cabin

Cabin 2

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