from django.shortcuts import render, HttpResponse, redirect


# Create your views here.
def index(request):
    return HttpResponse("To run the app use the link: <a href='/users'>Semi-Restful Users</a>")
