from django.test import TestCase
from ..models import User


class UserModelTest(TestCase):
    def test_create_user(self):
        email = "test@examples.com"
        first_name = "test"
        last_name = "example"
        phone_number = "+91 9876543200"
        password = "testpassword"

        user = User.objects.create(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.phone_number, phone_number)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_tenant)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        email = "admin@example.com"
        first_name = "admin"
        last_name = "example"
        phone_number = "+91 9812345671"
        username = "admin123"
        password = "admin1234321"
        user = User.objects.create_superuser(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            username=username,
        )
        user.set_password(password)
        user.save()

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)


class UserMethodTest(TestCase):
    def test_get_full_name(self):
        user = User(email="test@example.com", first_name="test",last_name="example")
        self.assertEqual(user.get_full_name(),"test example")
        
    def test_get_short_name(self):
        user=User(email="test@example.com",first_name="test")
        self.assertEqual(user.get_short_name(),"test")
        
