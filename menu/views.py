from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from menu.models import Menu
from menu.forms import MenuForm
from django.core import serializers
from warung.models import Warung  # Import the Warung model from warung app
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Create your views here.
def show_main(request):
    menu_entries = Menu.objects.all()
    context={
        "menu_entries":menu_entries
    }

    return render(request, "main.html", context)

def edit_menu(request, id):
    # Get the menu entry based on the id
    menu = get_object_or_404(Menu, pk=id)
    
    # Set the menu entry as an instance of the form
    form = MenuForm(request.POST or None, instance=menu)
    
    # Get all warungs to be displayed in the dropdown
    warungs = Warung.objects.all()

    if form.is_valid() and request.method == "POST":
        # Save form and redirect to the main page
        form.save()
        return HttpResponseRedirect(reverse('homepage:show_main'))

    context = {
        'form': form,
        'warungs': warungs,  # Pass warungs to the template
    }
    return render(request, "edit_menu.html", context)

def delete_menu(request, id):
    # Get mood berdasarkan id
    menus = Menu.objects.get(pk = id)
    # Hapus mood
    menus.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('homepage:show_main'))

def show_xml(request):
    data = Menu.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Menu.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def add_menu(request):
    form = MenuForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "add_menu.html", context)

@csrf_exempt
@require_POST
def add_menu_ajax(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Menu added successfully!"}, status=200)
        return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)