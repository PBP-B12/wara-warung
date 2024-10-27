from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Cart, CartItem, ChosenMenu
from menu.models import Menu

class MenuPlanningTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.cart = Cart.objects.create(user=self.user, name="Test Cart", budget=100000)
        self.menu_item = Menu.objects.create(menu="Test Menu Item", harga=10000, gambar="path/to/image.jpg")

    def test_add_item_to_cart(self):
        # Test adding an item to the cart with a specific price
        response = self.client.post(reverse("menuplanning:update_cart"), {
            'item_id': self.menu_item.id,
            'quantity': 1,
            'price': 10000,  
            'budget': 100000
        })
        self.assertEqual(response.status_code, 200)

        # Verify cart item attributes
        cart_item = CartItem.objects.get(cart=self.cart, item_name=self.menu_item.menu)
        self.assertEqual(cart_item.quantity, 1)
        self.assertEqual(cart_item.item_price, 10000)  
        
    def test_update_cart_item_quantity(self):
        # Test updating the quantity of an item already in the cart
        CartItem.objects.create(cart=self.cart, item_name=self.menu_item.menu, item_price=10000, quantity=1)

        response = self.client.post(reverse("menuplanning:update_cart"), {
            'item_id': self.menu_item.id,
            'quantity': 3,  # New quantity to update
            'price': 10000,
            'budget': 100000
        })
        self.assertEqual(response.status_code, 200)

        # Verify that quantity updated to 3
        cart_item = CartItem.objects.get(cart=self.cart, item_name=self.menu_item.menu)
        self.assertEqual(cart_item.quantity, 3)

    def test_exceeding_budget(self):
        # Test adding items that exceed the cart budget
        response = self.client.post(reverse("menuplanning:update_cart"), {
            'item_id': self.menu_item.id,
            'quantity': 15,  
            'price': 10000,
            'budget': 100000
        })
        self.assertEqual(response.status_code, 200)

        # Check if the response indicates a budget exceedance
        self.assertTrue(response.json()['exceeded_budget'])

    def test_save_chosen_menu(self):
        # Create a cart item and then test saving it as a chosen menu
        CartItem.objects.create(cart=self.cart, item_name=self.menu_item.menu, item_price=10000, quantity=1)
        
        response = self.client.post(reverse("menuplanning:confirm_save_cart"), {
            'budget': 100000
        })
        self.assertEqual(response.status_code, 200)

        # Verify chosen menu attributes
        chosen_menu = ChosenMenu.objects.get(user=self.user, item_name=self.menu_item.menu)
        self.assertEqual(chosen_menu.quantity, 1)
        self.assertEqual(chosen_menu.price, 10000)  

    def test_empty_cart(self):
        # Add an item to the cart and then empty it
        CartItem.objects.create(cart=self.cart, item_name=self.menu_item.menu, item_price=10000, quantity=1)

        response = self.client.post(reverse("menuplanning:empty_cart"))
        self.assertEqual(response.status_code, 200)

        # Verify the cart is emptied
        cart_items = CartItem.objects.filter(cart=self.cart, quantity__gt=0)
        self.assertEqual(cart_items.count(), 0)
