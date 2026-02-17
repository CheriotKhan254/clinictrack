from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView

from .models import Facility, LandRecord, Issue
from .forms import LandRecordForm, FacilityLocalityForm, IssueForm
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView


class HomeView(generic.TemplateView):
	template_name = "clinic/home.html"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx["facility_count"] = Facility.objects.count()
		ctx["landrecord_count"] = LandRecord.objects.count()
		ctx["issue_count"] = Issue.objects.count()
		return ctx


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
	login_url = "/login/"

	def test_func(self):
		return bool(self.request.user and self.request.user.is_staff)


class AdminDashboardView(AdminRequiredMixin, generic.TemplateView):
	"""
	Admin dashboard shown after login.
	From here you can navigate to facilities, land records, issues and patients.
	"""

	template_name = "clinic/admin_dashboard.html"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx["facility_count"] = Facility.objects.count()
		ctx["landrecord_count"] = LandRecord.objects.count()
		ctx["issue_count"] = Issue.objects.count()
		ctx["recent_facilities"] = Facility.objects.order_by("-created_at")[:5]
		return ctx


class LogoutView(generic.RedirectView):
	"""
	Log the user out then send them back to the home page.
	"""

	url = reverse_lazy("clinic:home")

	def get(self, request, *args, **kwargs):
		logout(request)
		return super().get(request, *args, **kwargs)


class AppLoginView(LoginView):
	"""
	Simple login page that sends staff users to the admin dashboard.
	"""

	template_name = "clinic/login.html"

	def get_success_url(self):
		return reverse_lazy("clinic:admin_dashboard")


# -------------------------
# Facility Views
# -------------------------
class FacilityListView(AdminRequiredMixin, generic.ListView):
    model = Facility
    template_name = "clinic/facility_list.html"
    context_object_name = "facilities"
    # paginate_by = 10  # optional

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset


class FacilityDetailView(AdminRequiredMixin, generic.DetailView):
	model = Facility
	template_name = "clinic/facility_detail.html"
	context_object_name = "facility"

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		# include an empty LandRecordForm so the facility detail template can embed it
		ctx["landrecord_form"] = LandRecordForm()
		# include a locality form prefilled with the facility instance
		ctx["locality_form"] = FacilityLocalityForm(instance=self.object)
		return ctx


class FacilityCreateView(AdminRequiredMixin, generic.CreateView):
	model = Facility
	fields = [
		"name",
		"location",
		"subcounty",
		"ward",
		"gps_x",
		"gps_y",
		"facility_type",
	]
	template_name = "clinic/facility_form.html"
	success_url = reverse_lazy("clinic:facility_list")


class FacilityUpdateView(AdminRequiredMixin, generic.UpdateView):
	model = Facility
	fields = [
		"name",
		"location",
		"subcounty",
		"ward",
		"gps_x",
		"gps_y",
		"facility_type",
	]
	template_name = "clinic/facility_form.html"
	success_url = reverse_lazy("clinic:facility_list")


class FacilityDeleteView(AdminRequiredMixin, generic.DeleteView):
	model = Facility
	template_name = "clinic/facility_confirm_delete.html"
	success_url = reverse_lazy("clinic:facility_list")


# -------------------------
# LandRecord Views
# -------------------------
class LandRecordListView(AdminRequiredMixin, generic.ListView):
    model = LandRecord
    template_name = "clinic/landrecord_list.html"
    context_object_name = "landrecords"
    # paginate_by = 10  # optional

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(
                facility__name__icontains=search
            )

        return queryset



class LandRecordDetailView(AdminRequiredMixin, generic.DetailView):
	model = LandRecord
	template_name = "clinic/landrecord_detail.html"
	context_object_name = "landrecord"


class LandRecordCreateView(AdminRequiredMixin, generic.CreateView):
	model = LandRecord
	fields = [
		"facility",
		"parcel_number",
		"owner",
		"acreage",
		"ownership_status",
		"document_type",
		"proprietorship",
		"land_use",
		"dispute_status",
		"planning_status",
		"survey_status",
		"acquisition_date",
		"registration_date",
		"encumbrances",
		"acquisition_amount",
		"fair_value",
		"disposal_date",
		"disposal_value",
		"annual_rental_income",
		"document",
	]
	template_name = "clinic/landrecord_form.html"
	success_url = reverse_lazy("clinic:landrecord_list")


class LandRecordCreateForFacilityView(AdminRequiredMixin, generic.CreateView):
	"""Create a LandRecord associated with a specific Facility (facility_pk in URL)."""
	model = LandRecord
	form_class = LandRecordForm
	template_name = "clinic/landrecord_form.html"

	def dispatch(self, request, *args, **kwargs):
		self.facility_pk = kwargs.get("facility_pk")
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		form.instance.facility_id = self.facility_pk
		return super().form_valid(form)

	def get_success_url(self):
		return reverse("clinic:facility_detail", kwargs={"pk": self.facility_pk})


class FacilityLocalityUpdateView(AdminRequiredMixin, generic.UpdateView):
	"""Update only the locality fields for a Facility (embedded on facility detail page)."""
	model = Facility
	form_class = FacilityLocalityForm
	template_name = "clinic/facility_locality_form.html"

	def get_success_url(self):
		return reverse("clinic:facility_detail", kwargs={"pk": self.object.pk})


class LandRecordUpdateView(AdminRequiredMixin, generic.UpdateView):
	model = LandRecord
	fields = [
		"facility",
		"parcel_number",
		"owner",
		"acreage",
		"ownership_status",
		"document_type",
		"proprietorship",
		"land_use",
		"dispute_status",
		"planning_status",
		"survey_status",
		"acquisition_date",
		"registration_date",
		"encumbrances",
		"acquisition_amount",
		"fair_value",
		"disposal_date",
		"disposal_value",
		"annual_rental_income",
		"document",
	]
	template_name = "clinic/landrecord_form.html"
	success_url = reverse_lazy("clinic:landrecord_list")


class LandRecordDeleteView(AdminRequiredMixin, generic.DeleteView):
	model = LandRecord
	template_name = "clinic/landrecord_confirm_delete.html"
	success_url = reverse_lazy("clinic:landrecord_list")


# -------------------------
# Issue Views
# -------------------------
class IssueListView(AdminRequiredMixin, generic.ListView):
	model = Issue
	template_name = "clinic/issue_list.html"
	context_object_name = "issues"


class IssueDetailView(AdminRequiredMixin, generic.DetailView):
	model = Issue
	template_name = "clinic/issue_detail.html"
	context_object_name = "issue"





class IssueUpdateView(AdminRequiredMixin, generic.UpdateView):
	model = Issue
	fields = ["facility", "description", "remarks", "recommendation", "status", "reported_by"]
	template_name = "clinic/issue_form.html"
	success_url = reverse_lazy("clinic:issue_list")


class IssueDeleteView(AdminRequiredMixin, generic.DeleteView):
	model = Issue
	template_name = "clinic/issue_confirm_delete.html"
	success_url = reverse_lazy("clinic:issue_list")


class IssueCreateView(AdminRequiredMixin, generic.CreateView):
    model = Issue
    form_class = IssueForm  # Use the ModelForm you defined
    template_name = "clinic/issue_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        facility_pk = self.kwargs.get('facility_pk')
        context['facility'] = get_object_or_404(Facility, pk=facility_pk)
        return context

    def form_valid(self, form):
        # Automatically link the issue to the facility
        facility_pk = self.kwargs.get('facility_pk')
        form.instance.facility = get_object_or_404(Facility, pk=facility_pk)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clinic:facility_detail', kwargs={'pk': self.object.facility.pk})


class IssueCreateForFacilityView(CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'clinic/issue_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.facility = get_object_or_404(Facility, pk=kwargs['facility_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facility'] = self.facility  # ← add this
        return context

    def form_valid(self, form):
        form.instance.facility = self.facility
        return super().form_valid(form)

    def get_success_url(self):
        return self.facility.get_absolute_url()


# -------------------------
# Patient Views
# -------------------------
