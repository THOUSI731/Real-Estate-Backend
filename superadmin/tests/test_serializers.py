from properties.models import Property, Unit
from rest_framework.test import APITestCase,APIClient
from ..api.serializers import PropertyPOSTSerializer
import pdb # Python Debugger

class PropertyPOSTSerializerTestCase(APITestCase):
    data = {
        "property_name": "thouseef_villa",
        "property_type": "home",
        "address": "abc villa 2nd street",
        "city": "calicut",
        "state": "example",
        "country": "elpamxe",
        "pin_code": "674560",
        "features": ["thoussi kjfke", "ndjls jjsd"],
    }

    def test_user_serializer_valid_data(self):
        serializer = PropertyPOSTSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_property_post_serializer_pin_code(self):
        serializer = PropertyPOSTSerializer(data=data)
        pdb.set_trace()
        self.assertTrue(serializer.is_valid())

