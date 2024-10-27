from django.test import TestCase, Client
from django.urls import reverse
from menu.models import Menu
from warung.models import Warung

class MenuAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a test Warung instance
        self.warung = Warung.objects.create(
            nama="Warung Test",
            alamat="Test Address",
            telepon=123456789
        )
        # Create a test Menu instance linked to the Warung
        self.menu_item = Menu.objects.create(
            warung=self.warung.nama,
            menu="Test Menu",
            harga=10000,
            gambar="test.jpg"
        )
        # URLs for testing
        self.add_url = reverse('menu:add_menu')
        self.edit_url = reverse('menu:edit_menu', args=[self.menu_item.id])
        self.delete_url = reverse('menu:delete_menu', args=[self.menu_item.id])
        self.ajax_url = reverse('menu:add_menu_ajax')
        self.main_url = reverse('menu:show_main')
        self.xml_url = reverse('menu:show_xml')
        self.json_url = reverse('menu:show_json')

    def test_show_main_page(self):
        """Test that the main page displays menu entries"""
        response = self.client.get(self.main_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "allmenu.html")
        self.assertContains(response, self.menu_item.menu)  # Check that the menu item is in HTML

    def test_add_menu(self):
        """Test adding a new menu item via form submission"""
        response = self.client.post(self.add_url, {
            'warung': self.warung.id,  # Use the foreign key ID
            'menu': 'New Menu Item',
            'harga': 20000,
            'gambar': 'new_image.jpg'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(Menu.objects.filter(menu='New Menu Item').exists())

    def test_add_menu_ajax(self):
        """Test adding a new menu item via AJAX"""
        response = self.client.post(self.ajax_url, {
            'warung': self.warung.id,  # Foreign key reference
            'menu': 'Ajax Menu Item',
            'harga': 15000,
            'gambar': 'ajax_image.jpg'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Menu added successfully!", response.json().get("message", ""))
        self.assertTrue(Menu.objects.filter(menu='Ajax Menu Item').exists())

    def test_edit_menu(self):
        """Test editing an existing menu item"""
        response = self.client.post(self.edit_url, {
            'warung': self.warung.id,
            'menu': 'Updated Menu',
            'harga': 12000,
            'gambar': 'updated.jpg'
        })
        self.assertEqual(response.status_code, 302)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.menu, 'Updated Menu')
        self.assertEqual(self.menu_item.harga, 12000)

    def test_delete_menu(self):
        """Test deleting a menu item"""
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Menu.objects.filter(id=self.menu_item.id).exists())

    def test_show_xml(self):
        """Test XML serialization of menu items"""
        response = self.client.get(self.xml_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], "application/xml")
        self.assertIn(self.menu_item.menu, response.content.decode())  # Check for menu item in XML

    def test_show_json(self):
        """Test JSON serialization of menu items"""
        response = self.client.get(self.json_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], "application/json")
        self.assertIn(self.menu_item.menu, response.json()[0]['fields']['menu'])  # Check for menu item in JSON