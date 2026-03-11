from django.core.exceptions import ObjectDoesNotExist
from netbox.plugins import PluginTemplateExtension

class LocationProfilePanel(PluginTemplateExtension):
    # This tells NetBox exactly which core model's view we want to modify
    model = 'dcim.location'

    # This tells NetBox to inject our code into the right column of the page
    def right_page(self):
        # Grab the current Location object being viewed
        location = self.context.get('object')
        
        # Check if this Location has a linked LocationProfile
        try:
            profile = location.profile
        except ObjectDoesNotExist:
            profile = None

        # Pass the profile to our custom HTML template
        return self.render('netbox_facilities/location_profile_panel.html', extra_context={
            'profile': profile,
        })

# Register the extension with NetBox
template_extensions = [LocationProfilePanel]