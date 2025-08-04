import os
from django.db.models.signals import post_migrate
from django.core.management import call_command
from django.dispatch import receiver
from djangoapp.models import CarMake  

@receiver(post_migrate)
def load_car_data(sender, **kwargs):
    fixture_path = os.path.join('djangoapp', 'fixtures', 'car_data.json')
    
    if os.path.exists(fixture_path):
        if not CarMake.objects.exists():  
            print("Loading car data from fixture...")
            call_command('loaddata', fixture_path)
        else:
            print("Car data already exists — skipping fixture load.")
