from decimal import Decimal

# 1. The Real-World Lookup Overrides
# Format: (from_unit, to_unit, input_value): output_value
UOM_LOOKUP_OVERRIDES = {
    'length': {
        # The classic floor tile override: 24 inches = exactly 600mm in DC parlance
        ('in', 'cm', Decimal('24')): Decimal('60'),
        ('cm', 'in', Decimal('60')): Decimal('24'),
        ('ft', 'm', Decimal('2')): Decimal('0.6'),
        ('m', 'ft', Decimal('0.6')): Decimal('2'),
    }
}

# 2. Strict Mathematical Multipliers (Converting everything to a Base Metric)
# Base Length: Meters | Base Area: Sq Meters | Base Weight: Kilograms | Base Load: kg/m²
CONVERSION_FACTORS = {
    'length': {
        'in': Decimal('0.0254'),
        'ft': Decimal('0.3048'),
        'mi': Decimal('1609.344'),
        'cm': Decimal('0.01'),
        'm': Decimal('1.0'),
        'km': Decimal('1000.0'),
    },
    'area': {
        'sqin': Decimal('0.00064516'),
        'sqft': Decimal('0.09290304'),
        'sqm': Decimal('1.0'),
    },
    'weight': {
        'oz': Decimal('0.0283495'),
        'lb': Decimal('0.453592'),
        't': Decimal('907.1847'),
        'g': Decimal('0.001'),
        'kg': Decimal('1.0'),
        'mt': Decimal('1000.0'),
    },
    'load': {
        'psf': Decimal('4.88243'),
        'kgm2': Decimal('1.0'),
        'kpa': Decimal('101.9716'),
    }
}

def convert_uom(category, value, from_unit, to_unit):
    """
    Safely converts a value between units, respecting industry lookup overrides.
    """
    if value is None or not from_unit or not to_unit:
        return None
        
    value = Decimal(str(value))
    
    # Return immediately if units match
    if from_unit == to_unit:
        return value

    # 1. Check the override lookup table first
    lookup_key = (from_unit, to_unit, value)
    if category in UOM_LOOKUP_OVERRIDES and lookup_key in UOM_LOOKUP_OVERRIDES[category]:
        return UOM_LOOKUP_OVERRIDES[category][lookup_key]

    # 2. Perform strict mathematical conversion
    factors = CONVERSION_FACTORS.get(category, {})
    if from_unit not in factors or to_unit not in factors:
        raise ValueError(f"Unsupported UoM conversion for category '{category}': {from_unit} -> {to_unit}")

    # Convert to base metric, then multiply out to target unit
    base_value = value * factors[from_unit]
    target_value = base_value / factors[to_unit]

    # Round to 4 decimal places for database storage safety
    return round(target_value, 4)