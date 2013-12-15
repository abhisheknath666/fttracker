from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count

from fttrackerapp.data_fetchers import FoodTruckDataFetcher

def index(request):
    message = """<h3>Welcome to Food Truck Tracker!</h3><p>We aggregate food truck visits around San Francisco's financial district.<br /><br /><a href="/pollfortrucks/">Click here</a> for a list of trucks participating in Off the grid over the last 30 days.</p>"""
    return HttpResponse(message)

def poll_for_trucks(request):
    # Use facebook's graph api to poll for trucks here
    appearances = FoodTruckDataFetcher().fetch_latest_data()
    context = {'appearances' : appearances}
    return render(request,'fttracker/summary.html', context)
