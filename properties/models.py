from django.db import models


class AbstractDate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Feature(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Property(AbstractDate):
    class PropertyType(models.TextChoices):
        HOME = "home", "Home"
        APARTMENT = "apartment", "Apartment"
        MANSION = "mansion", "Mansion"

    name = models.CharField(max_length=50)
    property_image = models.ImageField(
        upload_to="properties/",
        default="/media/properties/Homepage_desktop_b6361fc52d.jpg",
    )
    property_type = models.CharField(
        max_length=15, default=PropertyType.HOME, choices=PropertyType.choices
    )
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    pin_code = models.CharField(max_length=10)
    features = models.ManyToManyField(Feature, related_name="property_features")

    class Meta:
        verbose_name = "property"
        verbose_name_plural = "properties"

    def __str__(self) -> str:
        return self.name


class Unit(AbstractDate):
    class UnitType(models.TextChoices):
        ONEBHK = "1bhk", "1BHK"
        TWOBHK = "2bhk", "2BHK"
        THREEBHK = "3bhk", "3BHK"
        FOURBHK = "4bhk", "4BHK"

    class UnitStatus(models.TextChoices):
        AVAILABLE = "available", "Available"
        OCCUPIED = "occupied", "Occupied"

    property_reference = models.ForeignKey(
        Property, related_name="property_units", on_delete=models.CASCADE
    )
    unit_type = models.CharField(
        max_length=7, default=UnitType.ONEBHK, choices=UnitType.choices
    )
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.ManyToManyField(Feature, related_name="unit_features")
    unit_status = models.CharField(
        max_length=10, default=UnitStatus.AVAILABLE, choices=UnitStatus.choices
    )

    def __str__(self) -> str:
        return f"{self.property_reference.name} - {self.unit_type}"
