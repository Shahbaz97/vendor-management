from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Vendor, PurchaseOrder
# Create your tests here.
class VendorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'test@example.com',
            'address': '123 Test St',
            'vendor_code': 'TEST123'
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

    def test_get_vendor_list(self):
        url = reverse('vendor-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create_vendor(self):
    #     url = reverse('vendor-list-create')
    #     response = self.client.post(url, self.vendor_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_retrieve_vendor(self):
    #     url = reverse('vendor-retrieve-update-destroy', args=[self.vendor.id])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
