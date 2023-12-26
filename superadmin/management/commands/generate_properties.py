from django.core.management.base import BaseCommand, CommandParser
from faker import Faker

from properties.models import Property, Unit, Feature
from accounts.models import User
from tenants.models import Profile, TenantDocument

fake = Faker()


class Command(BaseCommand):
    help = "Generating Task"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("count", type=int, help="No of Data Needed to be Generated")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]

        for _ in range(count):
            Feature.objects.create(name=fake.name())
            feature = Feature.objects.filter(id=_ + 1).values_list("id",flat=True)
            feature_id = [x for x in feature]
            property_ = Property.objects.create(
                name=fake.name(),
                address=fake.address(),
                city=fake.city(),
                state=fake.state(),
                country=fake.country(),
                pin_code=fake.zipcode(),
            )
            property_.features.add(*feature_id)
            for _ in range(count // 2):
                unit_type = "1bhk"
                if _ % 2 == 0:
                    unit_type = "2bhk"
                if _ % 3 == 0:
                    unit_type = "3bhk"
                if _ % 4 == 0:
                    unit_type = "4bhk"
                unit_ = Unit.objects.create(
                    property_reference=property_,
                    unit_type=unit_type,
                    rent_cost=fake.random_int(min=1000, max=10000),
                    unit_status="available",
                )
                unit_.features.add(*feature_id)
        user = User.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            username=fake.name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            is_tenant=True,
        )
        Profile.objects.create(
            tenant=user,
            profile_picture="/media/properties/Homepage_desktop_b6361fc52d.jpg",
            address=fake.address(),
            city=fake.city(),
            state=fake.state(),
            country=fake.country(),
            pin_code=fake.zipcode(),
        )
        TenantDocument.objects.create(
            tenant=user,
            document_name="PAN",
            document_number="1234546731",
            document_image="/media/properties/Homepage_desktop_b6361fc52d.jpg",
            upload_date=fake.date(),
        )
        self.stdout.write(
            self.style.SUCCESS(f"{count} Data Generated Successfully")
        )
