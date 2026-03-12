from netbox.views import generic
from . import forms, models, tables

# 1. The Detail View (Looking at a single Location Profile)
class LocationProfileView(generic.ObjectView):
    queryset = models.LocationProfile.objects.all()

# 2. The Create/Edit View (The form page)
class LocationProfileEditView(generic.ObjectEditView):
    queryset = models.LocationProfile.objects.all()
    form = forms.LocationProfileForm

# 3. The Delete View (The confirmation page)
class LocationProfileDeleteView(generic.ObjectDeleteView):
    queryset = models.LocationProfile.objects.all()

# The List View (Looking at all Location Profiles)
class LocationProfileListView(generic.ObjectListView):
    queryset = models.LocationProfile.objects.all()
    table = tables.LocationProfileTable

# # --- Site Risk Profile Views ---
# class SiteRiskProfileListView(generic.ObjectListView):
#     queryset = models.SiteRiskProfile.objects.all()
#     table = tables.SiteRiskProfileTable # We will build this table next!

# class SiteRiskProfileView(generic.ObjectView):
#     queryset = models.SiteRiskProfile.objects.all()

# class SiteRiskProfileEditView(generic.ObjectEditView):
#     queryset = models.SiteRiskProfile.objects.all()
#     form = forms.SiteRiskProfileForm

# class SiteRiskProfileDeleteView(generic.ObjectDeleteView):
#     queryset = models.SiteRiskProfile.objects.all()

# # --- Site Profile Views ---
# class SiteProfileListView(generic.ObjectListView):
#     queryset = models.SiteProfile.objects.all()
#     table = tables.SiteProfileTable # We will build this table next!

# class SiteProfileView(generic.ObjectView):
#     queryset = models.SiteProfile.objects.all()

# class SiteProfileEditView(generic.ObjectEditView):
#     queryset = models.SiteProfile.objects.all()
#     form = forms.SiteProfileForm

# class SiteProfileDeleteView(generic.ObjectDeleteView):
#     queryset = models.SiteProfile.objects.all()