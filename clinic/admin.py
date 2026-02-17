from django.contrib import admin

from .models import Facility, LandRecord, Issue


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
	list_display = ("name", "location", "subcounty", "ward", "facility_type")
	search_fields = ("name", "location", "subcounty", "ward")
	list_filter = ("facility_type",)


@admin.register(LandRecord)
class LandRecordAdmin(admin.ModelAdmin):
	list_display = ("parcel_number", "owner", "facility", "acreage", "ownership_status", "survey_status")
	search_fields = ("parcel_number", "owner")
	list_filter = ("ownership_status", "survey_status")


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
	list_display = ("facility", "status", "reported_by", "created_at")
	search_fields = ("facility__name", "description")
	list_filter = ("status",)



