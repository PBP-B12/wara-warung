from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist, Section
from menu.models import Menu
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    sections = Section.objects.filter(user=request.user)  # Retrieve user's sections
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items, 'sections': sections})


@login_required
def add_section(request):
    if request.method == "POST":
        section_name = request.POST.get("section_name", "").strip()
        
        print("Received section_name:", section_name)  # Debug line
        
        # Check if the section name is provided and if it already exists
        if section_name:
            if not Section.objects.filter(user=request.user, name=section_name).exists():
                # Create the new section
                section = Section.objects.create(user=request.user, name=section_name)
                
                # Return the section's ID and name as JSON
                return JsonResponse({
                    'success': True,
                    'section_id': section.id,
                    'section_name': section.name
                })
            else:
                print("Section name already exists")  # Debug line
                return JsonResponse({
                    'success': False,
                    'error': 'Section name already exists.'
                }, status=400)
        else:
            print("Section name is missing")  # Debug line
            return JsonResponse({
                'success': False,
                'error': 'Section name is required.'
            }, status=400)

    print("Request method is not POST")  # Debug line
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

@login_required
def add_to_wishlist(request, menu_id):
    menu_item = get_object_or_404(Menu, id=menu_id)
    section_id = request.POST.get("section_id")
    section = None
    
    if section_id:
        section = get_object_or_404(Section, id=section_id, user=request.user)

    # Check if item already exists in the wishlist
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, menu=menu_item, defaults={'section': section})

    if created:
        messages.success(request, f'{menu_item.menu} has been added to your wishlist.')
    else:
        messages.info(request, f'{menu_item.menu} is already in your wishlist.')

    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    
    # Get the wishlist item and section
    wishlist_item = Wishlist.objects.filter(user=request.user, menu=menu).first()
    
    if wishlist_item:
        section = wishlist_item.section  # Save the section before deleting the item
        wishlist_item.delete()  # Remove the item from the wishlist
        
        # Check if the section has any remaining items
        if section and not Wishlist.objects.filter(user=request.user, section=section).exists():
            section.delete()  # Delete the section if no items remain in it
    
    return redirect('wishlist')

@login_required
def assign_section_to_wishlist_item(request, item_id):
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    
    if request.method == 'POST':
        section_id = request.POST.get('section_id')
        section = None
        
        if section_id:
            section = get_object_or_404(Section, id=section_id, user=request.user)
        
        wishlist_item.section = section
        wishlist_item.save()
        
        # Return a JSON response instead of redirecting
        return JsonResponse({"success": True, "section_name": section.name if section else "No Section"})

    return JsonResponse({"success": False, "error": "Invalid request method"})

@login_required
def delete_section(request, section_id):
    try:
        section = Section.objects.get(id=section_id, user=request.user)
        section.delete()
        return JsonResponse({"success": True})
    except Section.DoesNotExist:
        return JsonResponse({"success": False, "error": "Section not found."})


@login_required
def assign_section_to_wishlist_item(request, item_id):
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)

    if request.method == 'POST':
        section_id = request.POST.get('section')
        if section_id:
            section = get_object_or_404(Section, id=section_id, user=request.user)
            wishlist_item.section = section
            wishlist_item.save()
    
    return redirect('wishlist')