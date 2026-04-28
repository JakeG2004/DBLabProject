from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import Member, Uniform_Piece, Instrument, Rents_Uniform, Rents_Instrument, CLOTHING_CHOICES
from .forms import SignInForm, SignUpForm
import json

# Basic pages
def index(request):
    return render(request, "vmbsite/index.html")

def login_view(request):
    form = SignInForm(request, data=request.POST if request.method == 'POST' else None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('vmb:index')

    return render(request, 'vmbsite/login.html', {'form': form})

def signup_view(request):
    form = SignUpForm(data=request.POST if request.method == 'POST' else None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('vmb:index')

    return render(request, 'vmbsite/signup.html', {'form': form})

@login_required()
def logout_view(request):
    logout(request)
    return redirect('vmb:login')

# Easy access rental pages
@login_required()
def instrument(request):
    error = None
    success = None
    if request.method == 'POST':
        vandal_number = request.POST.get('vandal_number')
        instrument_id = request.POST.get('instrument_id')

        if not Member.objects.filter(vandal_number=vandal_number).exists():
            error = "Member not found."
        elif not Instrument.objects.filter(instrument_id=instrument_id).exists():
            error = "Instrument not found."
        elif Rents_Instrument.objects.filter(instrument_id=instrument_id).exists():
            error = "Instrument already rented."
        else:
            Rents_Instrument.objects.create(
                vandal_number_id=vandal_number,
                instrument_id_id=instrument_id
            )
            success = "Instrument rented successfully."

    return render(request, "vmbsite/instrument.html", {'error': error, 'success': success})

@login_required()
def uniform(request):
    def get_piece(errors, request, field, clothing_types, inst_name):
        field = request.POST.get(field)
        if field is None or field == '':
            return None
        # Assumes the field is supplied if required in the HTML
        if not Uniform_Piece.objects.filter(clothing_id=field, clothing_type__in=clothing_types).exists():
            errors.append(f'{inst_name} uniform piece not found.')
        elif Rents_Uniform.objects.filter(uniform_id=field).exists():
            errors.append(f'{inst_name} uniform piece already rented.')
        return field

    errors = []
    success = None
    if(request.method == 'POST'):
        # Check vandal number
        vandal_number = request.POST.get('vandal_number')
        if not Member.objects.filter(vandal_number=vandal_number).exists():
            errors.append('Member not found.')

        # Check uniform pieces
        shako_id = get_piece(errors, request, 'shako_id', ['perc_shako', 'horn_shako'], 'Shako')
        jacket_id = get_piece(errors, request, 'jacket_id', ['white_jacket', 'black_jacket', 'gritman_jacket'], 'Jacket')
        cape_id = get_piece(errors, request, 'cape_id', ['cape'], 'Cape')
        pants_id = get_piece(errors, request, 'pants_id', ['skirt', 'black_pants', 'white_pants'], 'Pants/Skirt')
        left_gauntlet_id = get_piece(errors, request, 'left_gauntlet_id', ['left_gauntlet'], 'Left gauntlet')
        right_gauntlet_id = get_piece(errors, request, 'right_gauntlet_id', ['right_gauntlet'], 'Right gauntlet')

        # Rent uniform pieces
        if not errors:
            for uniform_id in [shako_id, jacket_id, cape_id, pants_id, left_gauntlet_id, right_gauntlet_id]:
                if uniform_id is not None:
                    Rents_Uniform.objects.create(
                        vandal_number_id=vandal_number,
                        uniform_id_id=uniform_id,
                    )
            success='Uniform rented successfully.'

    return render(request, "vmbsite/uniform.html", {'errors': errors, 'success': success})

# Database pages
@login_required()
def database(request):
    if(request.method == 'POST'):
        pass

    return render(request, "vmbsite/database.html")

@login_required()
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

@login_required()
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

    valid_types = [v for _, items in CLOTHING_CHOICES for v, _ in items]
    return render(request, "vmbsite/uniform_db.html", {'uniforms': uniforms, 'clothing_choices': CLOTHING_CHOICES, 'valid_types': valid_types})

@login_required()
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

@login_required()
def instrument_rental_db(request):
    rentals = Rents_Instrument.objects.select_related('vandal_number', 'instrument_id').all()

    # Handle search
    query = request.GET.get('search_box', '').strip()
    if query:
        rentals = rentals.filter(
            # Search Member fields
            Q(vandal_number__vandal_number__icontains=query) | 
            Q(vandal_number__first_name__icontains=query) | 
            Q(vandal_number__last_name__icontains=query) |
            
            # Search Instrument fields
            Q(instrument_id__instrument_id__icontains=query) | 
            Q(instrument_id__instrument_type__icontains=query)
        )

    return render(request, "vmbsite/instrument_rental_db.html", {'rentals': rentals})

@login_required()
def uniform_rental_db(request):
    rentals = Rents_Uniform.objects.select_related('vandal_number', 'uniform_id').all()

    # Handle search
    query = request.GET.get('search_box', '').strip()
    if query:
        rentals = rentals.filter(
            # Search Member fields
            Q(vandal_number__vandal_number__icontains=query) | 
            Q(vandal_number__first_name__icontains=query) | 
            Q(vandal_number__last_name__icontains=query) |
            
            # Search Instrument fields
            Q(uniform_id__clothing_id__icontains=query) | 
            Q(uniform_id__clothing_type__icontains=query)
        )

    return render(request, "vmbsite/uniform_rental_db.html", {'rentals': rentals})

@login_required()
def import_uniform(request: HttpRequest) -> HttpResponse:
    return render(request, "vmbsite/import_uniform.html")

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