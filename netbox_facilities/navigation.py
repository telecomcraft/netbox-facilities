from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton

# 1. Define the "+" button (Color removed for NetBox 4.x compatibility)
location_profile_buttons = [
    PluginMenuButton(
        link='plugins:netbox_facilities:locationprofile_add',
        title='Add',
        icon_class='mdi mdi-plus-thick'
    )
]

# 2. Define the menu item (The clickable text in the sidebar)
location_profile_item = PluginMenuItem(
    link='plugins:netbox_facilities:locationprofile_list',
    link_text='Location Profiles',
    buttons=location_profile_buttons
)

# 3. Define the Top-Level Menu
menu = PluginMenu(
    label='Facilities',
    groups=(
        ('Architectural', (
            location_profile_item,
        )),
    ),
    icon_class='mdi mdi-domain' 
)