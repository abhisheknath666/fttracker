from django.shortcuts import render
from django.http import HttpResponse

import urllib2
import json

class Singleton(type):
    """
    Metaclass that defines a singleton
    """
    _classes = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._classes:
            cls._classes[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._classes[cls]

class FoodTruckDataFetcher:
    __metaclass__ = Singleton
    VENDORS_KEY = "\n\nVendors:"
    def __init__(self):
        self._access_token = "241089476057257|4ad1161cb5c438fa421944e69fea554a"

    def fetch_latest_data(self):
        otg_url = "https://graph.facebook.com/OffTheGridSF/events?access_token="+self._access_token
        # print "\nOTG url: "+otg_url
        while True:
            # Loop until we have all the latest
            # data.
            request = urllib2.Request(otg_url)
            response = urllib2.urlopen(request)
            response_json = json.loads(response.read()) # loads doesn't raise excpetions
            previously_parsed = self._parse_events(response_json)
            if previously_parsed:
                break

    def _parse_events(self, response_json):
        """
        For each event, get the associated food trucks
        """
        events = response_json["data"]
        for event in events:
            id = event["id"]
            previously_parsed = self._parse_event(id)
            if previously_parsed:
                return True

    def _parse_event(self, graph_id):
        """
        Here's where we parse the food trucks and location for the event
        """
        graph_url = "https://graph.facebook.com/"+graph_id+"?access_token="+self._access_token
        # print "\n ID url: "+graph_url
        request = urllib2.Request(graph_url)
        response = urllib2.urlopen(request)
        response_json = json.loads(response.read())
        description = response_json["description"]
        vendor_list = self._get_vendors(description)
        location = response_json["location"]
        # print "\nLocation: "+location
        return True

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
            return []
        vendors_substring = description[vendors_start_index:vendors_end_index]
        vendors_list = vendors_substring.split("\n")
        # print "\nVendors list: "+str(vendors_list)
        return vendors_list

def index(request):
    message = "App that tracks food trucks around San Francisco's financial district"
    return HttpResponse(message)

def poll_for_trucks(request):
    # Use facebook's graph api to poll for trucks here
    FoodTruckDataFetcher().fetch_latest_data()
    return HttpResponse("stub")
