import django_tables2 as tables
from netbox.tables import NetBoxTable
from .models import LocationProfile

class LocationProfileTable(NetBoxTable):
    # Make the Location name a clickable link
    location = tables.Column(
        linkify=True
    )
    
    class Meta(NetBoxTable.Meta):
        model = LocationProfile
        # The fields available to be shown in the table
        fields = (
            'pk', 'id', 'location', 'profile_type', 
            'area_square_feet', 'ceiling_height_feet',
            'floor_loading_capacity_psf', 'actions',
        )
        # The columns that show up by default when a user first loads the page
        default_columns = (
            'location', 'profile_type', 'area_square_feet', 
            'floor_loading_capacity_psf'
        )

# class SiteRiskProfileTable(NetBoxTable):
#     name = tables.Column(linkify=True)

#     class Meta(NetBoxTable.Meta):
#         model = SiteRiskProfile
#         fields = (
#             'pk', 'id', 'name', 'seismic_zone', 
#             'is_100_year_floodplain', 'flight_path_proximity', 
#             'rail_proximity', 'actions',
#         )
#         default_columns = ('name', 'seismic_zone', 'is_100_year_floodplain')

# class SiteProfileTable(NetBoxTable):
#     site = tables.Column(linkify=True)
#     risk_profile = tables.Column(linkify=True)

#     class Meta(NetBoxTable.Meta):
#         model = SiteProfile
#         fields = (
#             'pk', 'id', 'site', 'risk_profile', 
#             'total_building_area', 'total_building_area_unit', 'actions',
#         )
#         default_columns = ('site', 'risk_profile', 'total_building_area', 'total_building_area_unit')