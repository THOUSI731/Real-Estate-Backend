from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


# class PropertyListCreateAPIViewTestCase(APITestCase):
#     def test_property_create_view(self):
#         url = reverse("property-list-create")
#         data = {
#             "property_name": "thouseef_villa",
#             "property_type": "home",
#             "address": "abc villa 2nd street",
#             "city": "calicut",
#             "state": "example",
#             "country": "elpamxe",
#             "pin_code": "674560",
#             "features": ["thoussi kjfke", "ndjls jjsd"],
#         }
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["property_name"],"thouseef_villa")
#         self.assertEqual(response.data["property_type"],"home")
