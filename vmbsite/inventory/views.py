from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Member, Uniform_Piece, Instrument
import json

# Basic pages
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

# Easy access rental pages
def instrument(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/instrument.html")

def uniform(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/uniform.html")

# Database pages
def database(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/database.html")

def member_db(request):
    members = Member.objects.all()

    # Handle search
    query = request.GET.get('search_box', '').strip()
    if query:
        members = members.filter(
            Q(vandal_number__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(first_name__icontains=query)
        )

    return render(request, "vmbsite/member_db.html", {'members': members})

def uniform_db(request):
    uniforms = Uniform_Piece.objects.all()

    # Handle search
    query = request.GET.get('search_box', '').strip()
    if query:
        uniforms = uniforms.filter(
            Q(clothing_id__icontains=query) | 
            Q(size__icontains=query) | 
            Q(clothing_type__icontains=query)
        )

    return render(request, "vmbsite/uniform_db.html", {'uniforms': uniforms})

def instrument_db(request):
    instruments = Instrument.objects.all()

    # Handle search
    query = request.GET.get('search_box', '').strip()
    if query:
        instruments = instruments.filter(
            Q(instrument_id__icontains=query) | 
            Q(instrument_type__icontains=query)
        )

    return render(request, "vmbsite/instrument_db.html", {'instruments': instruments})

def instrument_rental_db(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/instrument_rental_db.html")

def uniform_rental_db(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/instrument_db.html")

# Member API endpoints
@require_POST
def update_member(request, pk):
    member = Member.objects.get(pk=pk)
    data = json.loads(request.body)
    member.first_name = data.get('first_name')
    member.last_name = data.get('last_name')
    member.save()

    return JsonResponse({'status': 'success', 'message': 'Member updated!'})

@require_POST
def delete_member(request, pk):
    member = Member.objects.get(pk=pk)
    member.delete()

    return JsonResponse({'status': 'success', 'message': 'Member deleted!'})

@require_POST
def add_member(request):
    data = request.POST
    vandal_id = data.get("vandal_id")

    if Member.objects.filter(vandal_number=vandal_id).exists():
        messages.error(request, f"Error: ID {vandal_id} already exists.")
    else:
        new_member = Member(
            vandal_number=vandal_id,
            first_name=data.get("first_name"),
            last_name=data.get("last_name")
        )
        new_member.save()
        messages.success(request, "Member added successfully!")

    return redirect('vmb:member_db')

# Uniform API endpoints
@require_POST
def update_uniform(request, pk):
    uniform = Uniform_Piece.objects.get(pk=pk)
    data = json.loads(request.body)
    uniform.size = data.get('clothing_size')
    uniform.clothing_type = data.get('clothing_type')
    uniform.save()

    return JsonResponse({'status': 'success', 'message': 'Uniform updated!'})

@require_POST
def delete_uniform(request, pk):
    uniform = Uniform_Piece.objects.get(pk=pk)
    uniform.delete()

    return JsonResponse({'status': 'success', 'message': 'Uniform deleted!'})

@require_POST
def add_uniform(request):
    data = request.POST
    clothing_id = data.get("uniform_id")

    if Uniform_Piece.objects.filter(clothing_id=clothing_id).exists():
        messages.error(request, f"Error: ID {clothing_id} already exists.")
    else:
        new_uniform = Uniform_Piece(
            clothing_id=clothing_id,
            size=data.get("uniform_size"),
            clothing_type=data.get("uniform_type")
        )
        new_uniform.save()
        messages.success(request, "Uniform piece added successfully!")

    return redirect('vmb:uniform_db')

# Instrument API endpoints
@require_POST
def update_instrument(request, pk):
    instrument = Instrument.objects.get(pk=pk)
    data = json.loads(request.body)
    instrument.type = data.get('instrument_type')
    instrument.notes = data.get('instrument_notes')
    instrument.save()

    return JsonResponse({'status': 'success', 'message': 'Instrument updated!'})

@require_POST
def delete_instrument(request, pk):
    instrument = Instrument.objects.get(pk=pk)
    instrument.delete()

    return JsonResponse({'status': 'success', 'message': 'Instrument deleted!'})

@require_POST
def add_instrument(request):
    data = request.POST
    instrument_id = data.get("inst_id")

    if Instrument.objects.filter(instrument_id=instrument_id).exists():
        messages.error(request, f"Error: ID {instrument_id} already exists.")
    else:
        new_instrument = Instrument(
            instrument_id=instrument_id,
            instrument_type=data.get("instrument_type"),
            notes=data.get("instrument_notes")
        )
        new_instrument.save()
        messages.success(request, "Instrument added successfully!")

    return redirect('vmb:instrument_db')