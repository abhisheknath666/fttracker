from django_cron import CronJobBase, Schedule
from fttrackerapp.data_fetchers import FoodTruckDataFetcher, GMT8
from datetime import datetime,date,timedelta,tzinfo
from fttrackerapp.singleton import Singleton

import urllib2,urllib

class HipChatCronJob(CronJobBase):
    """
    Posts food trucks appearing at the
    5th and Minna location every Wednesday
    and Friday at 11am
    """
    RUN_AT_TIMES = [ '11:00' ]
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, run_at_times=RUN_AT_TIMES)
    code = 'fttrackerapp.cron_jobs.HipChatCronJob'

    def __init__(self):
        self._api_key = "d332b671fbcccb43e857bb5e0e1430"
        self._room_id = "365644"

    def do(self):
        FoodTruckDataFetcher().fetch_latest_data()
        todays_date = datetime.now(GMT8())
        day_of_week = todays_date.date().weekday()
        location = "410 Minna St, San Francisco CA"
        if day_of_week==2 or day_of_week==4 or day_of_week==6:
            truck_set = FoodTruckDataFetcher().trucks_at_location(location)
            message = "Today at "+location+" we have: "
            for truck in truck_set:
                message = message + truck + ". "
            params = urllib.urlencode({'message' : message,
                                        'auth_token' : self._api_key,
                                        'room_id' : self._room_id,
                                        'from' : "FTTracker" })
            message_url = "https://api.hipchat.com/v1/rooms/message?"+params
            request = urllib2.Request(message_url)
            response = urllib2.urlopen(request)
