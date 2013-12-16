from django.shortcuts import render
from django.http import HttpResponse

from fttrackerapp.data_fetchers import FoodTruckDataFetcher

def index(request):
    message = """<h3>Welcome to Food Truck Tracker!</h3><p>We aggregate food truck visits around San Francisco's financial district.<br /><br /><a href="/pollfortrucks/">Click here</a> for a list of trucks participating in 'Off The Grid' over the last 30 days.</p>"""
    return HttpResponse(message)

def poll_for_trucks(request):
    """
    Call into our food truck data fetcher
    to retrieve a list of trucks making an
    appearance at Off the grid in the last
    30 days
    """
    appearances = FoodTruckDataFetcher().truck_visits_in_last_n_days(30)
    context = {'appearances' : appearances}
    return render(request,'fttracker/summary.html', context)

def trucks_at_location(request):
    """
    Returns a list of trucks
    currently at the specified location
    """
    location = request.GET.get('location')
    truck_set = FoodTruckDataFetcher().trucks_at_location(location)
    return HttpResponse(str(truck_set))
