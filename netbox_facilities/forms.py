from netbox.forms import NetBoxModelForm
from .models import LocationProfile, SiteRiskProfile, SiteProfile

class LocationProfileForm(NetBoxModelForm):
    class Meta:
        model = LocationProfile
        fields = (
            'location',
            'profile_type',
            'area_square_feet',
            'ceiling_height_feet',
            'floor_loading_capacity_psf',
            'tags',
        )

class SiteRiskProfileForm(NetBoxModelForm):
    class Meta:
        model = SiteRiskProfile
        fields = (
            'name', 'description', 'seismic_zone',
            'is_100_year_floodplain', 'flight_path_proximity',
            'rail_proximity', 'tags',
        )

class SiteProfileForm(NetBoxModelForm):
    class Meta:
        model = SiteProfile
        fields = (
            'site', 'risk_profile',
            'total_building_area', 'total_building_area_unit',
            'spatial_data', 'tags',
        )
