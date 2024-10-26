from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from wishlist.models import Wishlist, Section
from menu.models import Menu

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    sections = Section.objects.filter(user=request.user)  # Retrieve user's sections
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items, 'sections': sections})

@login_required
def add_section(request):
    if request.method == "POST":
        section_name = request.POST.get("section_name")
        # Check if a section with the same name exists for this user
        if section_name and not Section.objects.filter(user=request.user, name__iexact=section_name).exists():
            Section.objects.create(user=request.user, name=section_name)
            messages.success(request, f'Section "{section_name}" has been created.')
        else:
            messages.warning(request, f'Section "{section_name}" already exists.')
        return redirect('wishlist')


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
        
        return redirect('wishlist')

@login_required
def delete_section(request, section_id):
    section = get_object_or_404(Section, id=section_id, user=request.user)
    
    # Ensure no items are left in the section
    Wishlist.objects.filter(user=request.user, section=section).delete()
    
    # Delete the section itself
    section.delete()
    
    return redirect('wishlist')

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