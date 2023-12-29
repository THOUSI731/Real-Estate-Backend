from properties.models import Property, Unit
from rest_framework.test import APITestCase
from ..api.serializers import PropertyPOSTSerializer


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
        import copy

        data = copy.copy(self.data)
        data["pin_code"] = "1231"

        serializer = PropertyPOSTSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["pin_code"][0], "Pin code Must Be 6 digit number"
        )
