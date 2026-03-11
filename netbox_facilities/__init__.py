from netbox.plugins import PluginConfig

class FacilitiesConfig(PluginConfig):
    name = 'netbox_facilities'
    verbose_name = 'Netbox Facilities'
    description = 'Manage BICSI 002 Gray Space, Power, Cooling, and Architectural data'
    version = '0.1.0'
    base_url = 'facilities'
    author = 'Telecom Craft'
    
    # You can add default settings here later if needed
    default_settings = {}

# This tells NetBox to use the configuration class above
config = FacilitiesConfig