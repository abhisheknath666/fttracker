Welcome to food truck tracker (FTTracker)
=========
This is a Django web app that uses facebook graph calls to retrieve and store Food truck data for trucks that are part of the Off the Grid network.

Main components:

FoodTruckDataFetcher (data_fetchers.py). This is the class responsible for fetching the data from facebook and making it persistent.

HipChatCronJob (cron_jobs.py). This is the class responsible for sending scheduled hip chat messages with Food trucks appearing at a given location that day.

