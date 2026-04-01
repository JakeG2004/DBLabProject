from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "vmbsite/index.html")

def login(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/login.html")

def signup(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/signup.html")

def instrument(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/instrument.html")

def uniform(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/uniform.html")

def database(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/database.html")

def member_db(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/member_db.html")

def uniform_db(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/uniform_db.html")

def instrument_db(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/instrument_db.html")