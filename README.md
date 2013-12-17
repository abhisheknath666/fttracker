Welcome to food truck tracker (FTTracker)
=========
This is a Django web app that uses facebook graph calls to retrieve and store Food truck data for trucks that are part of the Off the Grid network.

Main components:

FoodTruckDataFetcher (data_fetchers.py). This is the class responsible for fetching the data from facebook and making it persistent.

HipChatCronJob (cron_jobs.py). This is the class responsible for sending scheduled hip chat messages with Food trucks appearing at a given location that day.

Work that remains to be done:
- Make facebook data requests asynchronous
- Write more comprehensive tests

Requirements:

Django==1.6.1
South==0.8.4
distribute==0.6.34
dj-database-url==0.2.2
dj-static==0.0.5
django-common-helpers==0.6.0
django-cron==0.3.3
django-toolbelt==0.0.1
gunicorn==18.0
psycopg2==2.5.1
static==0.4
wsgiref==0.1.2


Tech stack:
- Postgres db
- Gunicorn WSGI
- Django framework


