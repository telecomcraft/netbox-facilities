from django.test import TestCase
from .models import OperationalRequirementProfile

class OperationalRequirementProfileTest(TestCase):
    
    def test_standalone_creation(self):
        """Ensure the profile can be created without any sites attached."""
        profile = OperationalRequirementProfile.objects.create(
            name="Orphaned Template Profile",
            hours_per_week=40,
            weeks_per_year=50
        )
        # Verify it saved successfully and sites are empty
        self.assertEqual(profile.sites.count(), 0)
        self.assertEqual(profile.name, "Orphaned Template Profile")

    def test_catastrophic_level_4(self):
        """Test a 24/7/365 highly critical facility. Should yield Class 4."""
        profile = OperationalRequirementProfile(
            name="Core Banking DC",
            hours_per_week=168,
            weeks_per_year=52.14,
            extra_downtime_hours=0,
            max_annual_downtime='tier5', # Less than 5 mins
            impact_level='Catastrophic'
        )
        profile.calculate_metrics()
        
        self.assertEqual(profile.operational_level, 4)
        self.assertEqual(profile.availability_rank, 4)
        self.assertEqual(profile.availability_class, 4)

    def test_isolated_level_0(self):
        """Test a standard 40-hour work week office with high downtime tolerance."""
        profile = OperationalRequirementProfile(
            name="Branch Office",
            hours_per_week=40,
            weeks_per_year=50, # Lots of available maintenance window!
            max_annual_downtime='tier1', # > 5000 mins
            impact_level='Isolated'
        )
        profile.calculate_metrics()
        
        self.assertEqual(profile.operational_level, 0)
        self.assertEqual(profile.availability_rank, 0)
        self.assertEqual(profile.availability_class, 0)

    def test_partial_completion(self):
        """Ensure math safely pauses if a user hasn't selected an impact level yet."""
        profile = OperationalRequirementProfile(
            name="Incomplete Draft",
            hours_per_week=168,
            weeks_per_year=52.14,
            max_annual_downtime='tier3',
            impact_level='' # Left blank intentionally!
        )
        profile.calculate_metrics()
        
        # Operational Level and Rank should calculate, but final class should remain None
        self.assertEqual(profile.operational_level, 4)
        self.assertEqual(profile.availability_rank, 3) 
        self.assertIsNone(profile.availability_class)