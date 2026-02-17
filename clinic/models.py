from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# =========================
# Facility / Clinic Model
# =========================
class Facility(models.Model):
    FACILITY_TYPES = [
        ('Dispensary', 'Dispensary'),
        ('Health Center', 'Health Center'),
        ('Clinic', 'Clinic'),
        ('Hospital', 'Hospital'),
    ]

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    subcounty = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)

    gps_x = models.FloatField(null=True, blank=True)
    gps_y = models.FloatField(null=True, blank=True)

    facility_type = models.CharField(
        max_length=50,
        choices=FACILITY_TYPES,
        default='Clinic'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
         return reverse("clinic:facility_detail", kwargs={"pk": self.pk})


# =========================
# Land Record Model
# =========================
class LandRecord(models.Model):
    OWNERSHIP_STATUS = [
        ('Freehold', 'Freehold'),
        ('Leasehold', 'Leasehold'),
        ('Community', 'Community'),
        ('Government', 'Government'),
    ]

    DISPUTE_STATUS = [
        ('Disputed', 'Disputed'),
        ('Undisputed', 'Undisputed'),
    ]

    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="land_records"
    )

    parcel_number = models.CharField(max_length=100, blank=True)
    owner = models.CharField(max_length=200, blank=True)

    # Land size from the sheet (e.g. acres or hectares)
    acreage = models.FloatField()

    # Ownership details for the parcel
    ownership_status = models.CharField(
        max_length=50,
        choices=OWNERSHIP_STATUS,
        blank=True
    )

    # Free-text description of how the land is used
    land_use = models.CharField(max_length=255, blank=True)

    # Documented ownership details
    DOCUMENT_TYPES = [
        ("Title Deed", "Title Deed"),
        ("Certificate", "Certificate"),
        ("Allotment Letter", "Allotment Letter"),
        ("Other", "Other"),
    ]

    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPES,
        blank=True,
        help_text="Type of ownership document (title deed, certificate, allotment letter, other).",
    )

    proprietorship = models.CharField(
        max_length=255,
        blank=True,
        help_text="Proprietorship / ownership as per the document.",
    )

    # Whether the land is disputed or undisputed (from Excel column)
    dispute_status = models.CharField(
        max_length=20,
        choices=DISPUTE_STATUS,
        blank=True
    )

    # Planned / unplanned settlement
    PLANNING_STATUS = [
        ("Planned", "Planned"),
        ("Unplanned", "Unplanned"),
    ]

    planning_status = models.CharField(
        max_length=20,
        choices=PLANNING_STATUS,
        blank=True,
    )

    # Survey status (True = surveyed, False = not surveyed)
    survey_status = models.BooleanField(default=False)

    acquisition_date = models.DateField(null=True, blank=True)
    registration_date = models.DateField(null=True, blank=True)

    encumbrances = models.TextField(
        blank=True,
        help_text="Any encumbrances on the land.",
    )

    acquisition_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Acquisition amount for the land.",
    )

    fair_value = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Fair value / land index.",
    )

    disposal_date = models.DateField(
        null=True,
        blank=True,
        help_text="Disposal date / change of use date.",
    )

    disposal_value = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Disposal value.",
    )

    annual_rental_income = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Annual rental income from the land.",
    )

    document = models.FileField(
        upload_to="land_documents/",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.parcel_number} - {self.facility.name}"


# =========================
# Issue / Observation Model
# =========================
class Issue(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    ]

    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="issues"
    )

    # Observation / issue on the land
    description = models.TextField(help_text="Observation / issue on the land.")
    # General remarks
    remarks = models.TextField(blank=True)
    # Recommendation on land
    recommendation = models.TextField(blank=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Open'
    )

    reported_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issue - {self.facility.name}"


