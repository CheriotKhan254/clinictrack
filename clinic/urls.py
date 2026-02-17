from django.urls import path
from . import views

app_name = "clinic"

urlpatterns = [
    # Home & Authentication
    path("", views.HomeView.as_view(), name="home"),
    path("login/", views.AppLoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.AdminDashboardView.as_view(), name="admin_dashboard"),

    # Facility URLs
    path("facilities/", views.FacilityListView.as_view(), name="facility_list"),
    path("facility/add/", views.FacilityCreateView.as_view(), name="facility_add"),
    path("facility/<int:pk>/", views.FacilityDetailView.as_view(), name="facility_detail"),
    path("facility/<int:pk>/edit/", views.FacilityUpdateView.as_view(), name="facility_edit"),
    path("facility/<int:pk>/delete/", views.FacilityDeleteView.as_view(), name="facility_delete"),
    path("facility/<int:pk>/locality/edit/", views.FacilityLocalityUpdateView.as_view(), name="facility_locality_edit"),
    path("facility/<int:facility_pk>/land/add/", views.LandRecordCreateForFacilityView.as_view(), name="facility_land_add"),
    path("facility/<int:facility_pk>/issues/add/", views.IssueCreateForFacilityView.as_view(), name="issue_add"),

    # LandRecord URLs
    path("landrecords/", views.LandRecordListView.as_view(), name="landrecord_list"),
    path("landrecords/add/", views.LandRecordCreateView.as_view(), name="landrecord_add"),
    path("landrecords/<int:pk>/", views.LandRecordDetailView.as_view(), name="landrecord_detail"),
    path("landrecords/<int:pk>/edit/", views.LandRecordUpdateView.as_view(), name="landrecord_edit"),
    path("landrecords/<int:pk>/delete/", views.LandRecordDeleteView.as_view(), name="landrecord_delete"),

    # Issue URLs
    path("issues/", views.IssueListView.as_view(), name="issue_list"),
    path("issues/<int:pk>/", views.IssueDetailView.as_view(), name="issue_detail"),
    path("issues/<int:pk>/edit/", views.IssueUpdateView.as_view(), name="issue_edit"),
    path("issues/<int:pk>/delete/", views.IssueDeleteView.as_view(), name="issue_delete"),

   
]
