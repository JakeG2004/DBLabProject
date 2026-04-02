from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Member
import json

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
    if request.method == 'POST':
        data = request.POST
        v_id = data.get("vandal_id")

        # Check that this vandal# doesnt already exist
        if Member.objects.filter(vandal_number=v_id).exists():
            messages.error(request, f"Error: A member with Vandal ID {v_id} already exists.")
            
            # Return the same page so they can see the error
            return render(request, "vmbsite/member_db.html", {
                'members': Member.objects.all()
            })

        # Add new member if they don't already exist
        new_member = Member()
        new_member.vandal_number = v_id
        new_member.first_name = data.get("first_name")
        new_member.last_name = data.get("last_name")
        new_member.save()

        # Redirect with success message
        messages.success(request, "Member added successfully!")
        return redirect('vmb:member_db')

    # Search feature
    members = Member.objects.all()
    if request.method == 'GET':
        data = request.GET
        query = data.get('search_box')
        if(query):
            members = members.filter(
                Q(vandal_number__icontains=query) | 
                Q(first_name__icontains=query) | 
                Q(last_name__icontains=query)
            )

    # Return the search
    return render(request, "vmbsite/member_db.html", {'members': members})

def uniform_db(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/uniform_db.html")

def instrument_db(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/instrument_db.html")

def instrument_rental_db(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/instrument_rental_db.html")

def uniform_rental_db(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/instrument_db.html")

@require_POST
def update_member(request, pk):
    member = Member.objects.get(pk=pk)
    data = json.loads(request.body) # Parse JSON from JS fetch
    member.first_name = data.get('first_name')
    member.last_name = data.get('last_name')
    member.save()
    return JsonResponse({'status': 'success'})

@require_POST
def delete_member(request, pk):
    member = Member.objects.get(pk=pk)
    member.delete()
    return JsonResponse({'status': 'success'})