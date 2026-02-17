from django import forms
from .models import LandRecord, Facility, Issue


class LandRecordForm(forms.ModelForm):
    class Meta:
        model = LandRecord
        # exclude facility because the form will be scoped to a facility
        exclude = ["facility", "created_at"]

        widgets = {
            "acquisition_date": forms.DateInput(attrs={"type": "date"}),
            "registration_date": forms.DateInput(attrs={"type": "date"}),
            "disposal_date": forms.DateInput(attrs={"type": "date"}),
        }


class FacilityLocalityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ["location", "subcounty", "ward", "gps_x", "gps_y", "facility_type"]
        widgets = {
            "gps_x": forms.NumberInput(attrs={"step": "any"}),
            "gps_y": forms.NumberInput(attrs={"step": "any"}),
        }


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['status', 'description', 'remarks', 'recommendation']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'recommendation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }