from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    message = "App that tracks food trucks around San Francisco's financial district"
    return HttpResponse(message)

def pollfortrucks(request):
    # Use facebook's graph api to poll for trucks here
    return HttpResponse("stub")
