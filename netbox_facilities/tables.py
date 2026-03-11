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