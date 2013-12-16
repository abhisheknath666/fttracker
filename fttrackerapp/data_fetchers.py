from fttrackerapp.models import FoodTruck, Location, Appearance
from fttrackerapp.singleton import Singleton

from datetime import datetime,date,timedelta,tzinfo
import urllib2
import json
import time

class GMT8(tzinfo):
    __metaclass__=Singleton
    def utcoffset(self,dt):
        return timedelta(hours=-8)
    def tzname(self,dt):
        return "GMT -8"
    def dst(self, dt):
        return timedelta(0)

class FoodTruckDataFetcher:
    """
    Singleton class that fetches and stores
    food truck data from Facebook's Off The Grid
    page
    """
    __metaclass__ = Singleton
    VENDORS_KEY = "\n\nVendors:"

    def __init__(self):
        self._access_token = "241089476057257|4ad1161cb5c438fa421944e69fea554a"

    def fetch_latest_data(self):
        """
        Fetch the latest food truck data with a graph call
        """
        limit = 100 # It's unlikely we'll have more than a 100 events since the last call
        otg_url = "https://graph.facebook.com/OffTheGridSF/events?"+"limit="+str(limit)+"&access_token="+self._access_token

        while True:
            # Loop until we have all the latest
            # data.
            request = urllib2.Request(otg_url)
            response = urllib2.urlopen(request)
            response_json = json.loads(response.read()) # loads doesn't raise excpetions
            previously_parsed = self._parse_events(response_json)
            if previously_parsed:
                break
            paging_info = response_json.get("paging")
            otg_url = paging_info.get("next")
            if not otg_url:
                break

    def truck_visits_in_last_n_days(self, n):
        """
        Convenience method to fetch the latest data and for each truck count
        the number of visits in the last 'n' days
        """
        self.fetch_latest_data()
        todays_date = datetime.now(GMT8()).date()
        thirty_days_ago = todays_date+timedelta(days=-n)
        filtered_appearances = Appearance.objects.filter(date__gte=thirty_days_ago, date__lt=todays_date)
        truck_appearances = []
        for truck in FoodTruck.objects.all():  # Smaller number of food trucks means it's more performant than using .iterator()
            truck_appearance = {}
            number_of_appearances = filtered_appearances.filter(truck__name=truck.name).count()
            if number_of_appearances==0:
                continue
            truck_appearance['number_of_appearances'] = number_of_appearances
            truck_appearance['name'] = truck.name
            truck_appearances.append(truck_appearance)

        truck_appearances = sorted(truck_appearances, key=lambda appearance: appearance['number_of_appearances'], reverse=True)
        return truck_appearances

    def trucks_at_location(self, location):
        """
        Convenience method that returns a list of trucks
        present at 'location' today
        """
        todays_date = datetime.now(GMT8()).date()
        appearances = Appearance.objects.filter(location__name=location, date=todays_date)
        truck_set = { appearances.truck.name for appearances in appearances }
        return truck_set

    def _parse_events(self, response_json):
        """
        For each event, get the associated food trucks
        """
        events = response_json.get("data")
        for event in events:
            id = event.get("id")
            previously_parsed = self._parse_event(id)
            if previously_parsed:
                return True

    def _parse_event(self, graph_id):
        """
        Here's where we parse the food trucks and location for the event
        """
        graph_url = "https://graph.facebook.com/"+graph_id+"?access_token="+self._access_token
        request = urllib2.Request(graph_url)
        response = urllib2.urlopen(request)
        response_json = json.loads(response.read())
        description = response_json.get("description")
        location = response_json.get("location")
        vendor_list = self._get_vendors(description)
        date_str = response_json.get("start_time") # TODO: if end_time-start_time>1 day create new appearance?
        date_end_index = date_str.find("T") # 2013-12-20T17:00:00-0800
        if date_end_index==-1:
            print "Failed to parse event: "+graph_id
            return False
        date_str = date_str[:date_end_index]
        try:
            appearance_datetime = datetime.strptime(date_str,"%Y-%m-%d")
            appearance_date = appearance_datetime.date()
        except ValueError:
            print "Failed to parse event: "+graph_id
            return False
        return self._make_persistent(location, vendor_list, appearance_date)

    def _make_persistent(self, location, vendor_list, date):
        """
        Store parsed data in the db
        """
        location_obj = None
        if not location=='':
            location_obj, created = Location.objects.get_or_create(name=location)
        if not location_obj:
            return

        for vendor in vendor_list:
            if vendor=='':
                continue
            truck_obj, t_created = FoodTruck.objects.get_or_create(name=vendor)
            appearance_obj, a_created = Appearance.objects.get_or_create(truck=truck_obj,location=location_obj, date=date)
            if not a_created:
                # We've already parsed this event
                return True
        return False

    def _get_vendors(self, description):
        """
        Parse the vendors out of the description string
        """
        # print "\nDescription: "+description
        vendors_start_index = description.find(FoodTruckDataFetcher.VENDORS_KEY)
        if vendors_start_index == -1:
            return []
        vendors_start_index += len(FoodTruckDataFetcher.VENDORS_KEY)
        vendors_end_index = description.find("\n\n",vendors_start_index);
        if vendors_end_index == -1:
            vendors_end_index = len(description)
        vendors_substring = description[vendors_start_index:vendors_end_index]
        vendors_list = vendors_substring.split("\n")
        normalized_list = []
        for vendor in vendors_list:
            vendor = vendor.lstrip()
            vendor = vendor.rstrip()
            normalized_list.append(vendor)
        # print "\nVendors list: "+str(vendors_list)
        return normalized_list
