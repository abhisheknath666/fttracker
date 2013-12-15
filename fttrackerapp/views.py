from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count

from fttrackerapp.data_fetchers import FoodTruckDataFetcher

def index(request):
    message = "App that tracks food trucks around San Francisco's financial district"
    return HttpResponse(message)

def poll_for_trucks(request):
    # Use facebook's graph api to poll for trucks here
    appearances = FoodTruckDataFetcher().fetch_latest_data()
    context = {'appearances' : appearances}
    return render(request,'fttracker/summary.html', context)
