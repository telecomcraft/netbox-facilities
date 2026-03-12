from decimal import Decimal

from django.db import models
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet


class LengthUnitChoices(ChoiceSet):
    # Imperial
    UNIT_INCH = 'in'
    UNIT_FOOT = 'ft'
    UNIT_MILE = 'mi'
    # Metric
    UNIT_CENTIMETER = 'cm'
    UNIT_METER = 'm'
    UNIT_KILOMETER = 'km'

    CHOICES = (
        ('Imperial', (
            (UNIT_INCH, 'Inches (in)'),
            (UNIT_FOOT, 'Feet (ft)'),
            (UNIT_MILE, 'Miles (mi)'),
        )),
        ('Metric', (
            (UNIT_CENTIMETER, 'Centimeters (cm)'),
            (UNIT_METER, 'Meters (m)'),
            (UNIT_KILOMETER, 'Kilometers (km)'),
        )),
    )

class AreaUnitChoices(ChoiceSet):
    UNIT_SQ_IN = 'sqin'
    UNIT_SQ_FT = 'sqft'
    UNIT_SQ_M = 'sqm'

    CHOICES = (
        ('Imperial', (
            (UNIT_SQ_IN, 'Square Inches (sq in)'),
            (UNIT_SQ_FT, 'Square Feet (sq ft)'),
        )),
        ('Metric', (
            (UNIT_SQ_M, 'Square Meters (sq m)'),
        )),
    )

class StructuralLoadUnitChoices(ChoiceSet):
    UNIT_PSF = 'psf'
    UNIT_KGM2 = 'kgm2'
    UNIT_KPA = 'kpa' # Kilopascals are also common in international structural engineering

    CHOICES = (
        ('Imperial', (
            (UNIT_PSF, 'Pounds per Sq. Foot (psf)'),
        )),
        ('Metric', (
            (UNIT_KGM2, 'Kilograms per Sq. Meter (kg/m²)'),
            (UNIT_KPA, 'Kilopascals (kPa)'),
        )),
    )


class WeightUnitChoices(ChoiceSet):
    # TODO: Consolidate with other unit code in utils
    # Standalone Weights
    UNIT_OUNCE = 'oz'
    UNIT_POUND = 'lb'
    UNIT_TON = 't' # Short ton
    UNIT_GRAM = 'g'
    UNIT_KILOGRAM = 'kg'
    UNIT_METRIC_TON = 'mt'
    
    # Distributed Structural Loads
    UNIT_PSF = 'psf'
    UNIT_KGM2 = 'kgm2'
    UNIT_KPA = 'kpa'

    CHOICES = (
        ('Imperial Mass', (
            (UNIT_OUNCE, 'Ounces (oz)'),
            (UNIT_POUND, 'Pounds (lb)'),
            (UNIT_TON, 'Tons (t)'),
        )),
        ('Metric Mass', (
            (UNIT_GRAM, 'Grams (g)'),
            (UNIT_KILOGRAM, 'Kilograms (kg)'),
            (UNIT_METRIC_TON, 'Metric Tons (mt)'),
        )),
        ('Structural Load (Imperial)', (
            (UNIT_PSF, 'Pounds per Sq. Foot (psf)'),
        )),
        ('Structural Load (Metric)', (
            (UNIT_KGM2, 'Kilograms per Sq. Meter (kg/m²)'),
            (UNIT_KPA, 'Kilopascals (kPa)'),
        )),
    )


class OperationalRequirementProfile(NetBoxModel):
    """Creates a BICSI 002 operational requirement profile that can be used to calculate
    an availability class and apply it to one or more sites."""

    name = models.CharField(
        max_length=100, 
        unique=True,
        help_text="e.g., 'Standard Regional Campus', 'Tier 4 Core Data Center'"
    )
    sites = models.ManyToManyField(
        to='dcim.Site', 
        blank=True, 
        related_name='operational_requirements',
        help_text="The site(s) this reliability profile applies to."
    )

    # --- Step 1: Production Inputs ---
    hours_per_week = models.DecimalField(max_digits=5, decimal_places=2, default=168)
    weeks_per_year = models.DecimalField(max_digits=4, decimal_places=2, default=52.14)
    extra_downtime_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    # --- Step 2 & 3: Lookup Inputs ---
    max_annual_downtime = models.CharField(max_length=50, blank=True, null=True)
    impact_level = models.CharField(max_length=50, blank=True, null=True)

    # --- Calculated Outputs (Stored permanently) ---
    operational_level = models.IntegerField(null=True, blank=True)
    availability_rank = models.IntegerField(null=True, blank=True)
    availability_class = models.IntegerField(null=True, blank=True)

    # Lookup Matrices built directly into the class based on BICSI 002 Tables B-2 and B-4
    RANK_MATRIX = {
        0: {'tier1': 0, 'tier2': 0, 'tier3': 1, 'tier4': 2, 'tier5': 2},
        1: {'tier1': 0, 'tier2': 1, 'tier3': 2, 'tier4': 2, 'tier5': 2},
        2: {'tier1': 1, 'tier2': 2, 'tier3': 2, 'tier4': 2, 'tier5': 3},
        3: {'tier1': 2, 'tier2': 2, 'tier3': 2, 'tier4': 3, 'tier5': 4},
        4: {'tier1': 3, 'tier2': 3, 'tier3': 3, 'tier4': 4, 'tier5': 4},
    }

    CLASS_MATRIX = {
        'Isolated':     {0: 0, 1: 0, 2: 1, 3: 3, 4: 3},
        'Minor':        {0: 0, 1: 1, 2: 2, 3: 3, 4: 3},
        'Major':        {0: 1, 1: 2, 2: 2, 3: 3, 4: 3},
        'Severe':       {0: 1, 1: 2, 2: 3, 3: 3, 4: 4},
        'Catastrophic': {0: 1, 1: 2, 2: 3, 3: 4, 4: 4},
    }

    class Meta:
        ordering = ('name',)

    def __str__(self):
        if self.availability_class is not None:
            return f"{self.name} (Class {self.availability_class})"
        return f"{self.name} (Incomplete)"

    def calculate_metrics(self):
        """Runs the BICSI 002 math and updates the model's fields."""
        # 1. Step 1 Math: Determine Operational Level
        prod_hours = float(self.hours_per_week) * float(self.weeks_per_year)
        maint_hours = (8760 - prod_hours) + float(self.extra_downtime_hours)
        
        if maint_hours >= 400: self.operational_level = 0
        elif maint_hours >= 100: self.operational_level = 1
        elif maint_hours >= 50: self.operational_level = 2
        elif maint_hours >= 1: self.operational_level = 3
        else: self.operational_level = 4

        # 2. Step 2 & 3 Lookups (Only run if the user selected the dropdowns)
        self.availability_rank = None
        self.availability_class = None

        if self.max_annual_downtime and self.max_annual_downtime in self.RANK_MATRIX[self.operational_level]:
            self.availability_rank = self.RANK_MATRIX[self.operational_level][self.max_annual_downtime]

            if self.impact_level and self.impact_level in self.CLASS_MATRIX:
                self.availability_class = self.CLASS_MATRIX[self.impact_level][self.availability_rank]

    def save(self, *args, **kwargs):
        """Automatically recalculate before saving to the database."""
        self.calculate_metrics()
        super().save(*args, **kwargs)


class SiteRiskProfile(NetBoxModel):
    """The Risk Profile (Standalone Model)"""
    name = models.CharField(
        max_length=100, 
        unique=True,
        help_text="e.g., 'US East Coast - Hurricane Zone', 'NorCal Seismic'"
    )
    description = models.CharField(
        max_length=200, 
        blank=True
    )
    
    # BICSI 002 Chapter 5: Site Selection Risk Factors
    seismic_zone = models.CharField(
        max_length=50, blank=True, 
        help_text="Applicable seismic zone or category (e.g., Zone 4, Category D)"
    )
    is_100_year_floodplain = models.BooleanField(
        default=False, 
        help_text="Is the site located within a 100-year floodplain?"
    )
    flight_path_proximity = models.BooleanField(
        default=False, 
        help_text="Is the site within 5 miles of a major commercial flight path?"
    )
    rail_proximity = models.BooleanField(
        default=False, 
        help_text="Is the site within 1 mile of a major rail line or highway?"
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class SiteProfile(NetBoxModel):
    """The Site Profile (Extends native dcim.Site)"""
    site = models.OneToOneField(
        to='dcim.Site', on_delete=models.CASCADE, related_name='profile'
    )
    risk_profile = models.ForeignKey(
        to='SiteRiskProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='sites'
    )
    
    # 1. The User-Facing Fields (What they type into the UI)
    total_building_area = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Total gross area of the facility"
    )
    total_building_area_unit = models.CharField(
        max_length=50,
        choices=AreaUnitChoices,
        default=AreaUnitChoices.UNIT_SQ_FT,
        blank=True,
    )
    
    # 2. The Hidden Base Field (Always stores strictly in Square Meters)
    _total_building_area_sqm = models.DecimalField(
        max_digits=12, decimal_places=4, null=True, blank=True,
        editable=False # This flag guarantees it never accidentally shows up in a NetBox web form!
    )
    
    spatial_data = models.JSONField(
        null=True, blank=True,
        help_text="Valid GeoJSON representation of the site boundaries"
    )

    class Meta:
        ordering = ('site',)

    def __str__(self):
        return f"{self.site.name} Architectural Profile"

    # 3. Intercept the Save Process
    def save(self, *args, **kwargs):
        # If the user typed in an area, instantly calculate the base Square Meter value
        if self.total_building_area and self.total_building_area_unit:
            self._total_building_area_sqm = convert_uom(
                category='area',
                value=self.total_building_area,
                from_unit=self.total_building_area_unit,
                to_unit=AreaUnitChoices.UNIT_SQ_M # Our strict base unit
            )
        else:
            self._total_building_area_sqm = None

        # Pass the data back to Django's core system to actually write it to PostgreSQL
        super().save(*args, **kwargs)

    # 4. (Optional) Quick-access property for API use later
    @property
    def area_in_sqft(self):
        """Allows API serializers to easily fetch the strict SqFt value, regardless of what the user entered"""
        if not self._total_building_area_sqm:
            return None
        return convert_uom('area', self._total_building_area_sqm, AreaUnitChoices.UNIT_SQ_M, AreaUnitChoices.UNIT_SQ_FT)


class LocationProfileTypeChoices(ChoiceSet):
    TYPE_FLOOR = 'floor'
    TYPE_ROOM = 'room'
    TYPE_HAC = 'hac' # Hot Aisle Containment
    TYPE_CAC = 'cac' # Cold Aisle Containment
    TYPE_ZONE = 'zone' # General MEP/Fire Zone
    
    CHOICES = (
        (TYPE_FLOOR, 'Floor'),
        (TYPE_ROOM, 'Room'),
        (TYPE_HAC, 'Hot Aisle Containment'),
        (TYPE_CAC, 'Cold Aisle Containment'),
        (TYPE_ZONE, 'Zone'),
    )


class LocationProfile(NetBoxModel):
    # The magical link to NetBox's built-in Location
    location = models.OneToOneField(
        to='dcim.Location',
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # The Structural Designation
    profile_type = models.CharField(
        max_length=50,
        choices=LocationProfileTypeChoices,
        default=LocationProfileTypeChoices.TYPE_ROOM,
        help_text="The architectural designation of this location space"
    )
    
    # Spatial Metrics (for your BICSI volume/capacity calculations)
    area_square_feet = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Usable area in square feet"
    )
    ceiling_height_feet = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Height from finished floor to dropped ceiling or deck"
    )
    
    # Structural Limits
    floor_loading_capacity_psf = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Maximum structural floor load limit (lbs/sqft)"
    )

    class Meta:
        ordering = ('location',)

    def __str__(self):
        return f"{self.location.name} ({self.get_profile_type_display()})"