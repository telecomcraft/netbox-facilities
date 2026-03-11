from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from . import models, views

urlpatterns = [
    # The List View
    path('location-profiles/', views.LocationProfileListView.as_view(), name='locationprofile_list'),
    
    # The Detail View (Looking at a specific profile)
    path('location-profiles/<int:pk>/', views.LocationProfileView.as_view(), name='locationprofile'),
    
    # The Create/Add View
    path('location-profiles/add/', views.LocationProfileEditView.as_view(), name='locationprofile_add'),
    
    # The Edit View
    path('location-profiles/<int:pk>/edit/', views.LocationProfileEditView.as_view(), name='locationprofile_edit'),
    
    # The Delete View
    path('location-profiles/<int:pk>/delete/', views.LocationProfileDeleteView.as_view(), name='locationprofile_delete'),
    
    # The built-in Change Log View (NetBox gives us this for free!)
    path('location-profiles/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='locationprofile_changelog', kwargs={'model': models.LocationProfile}),
]