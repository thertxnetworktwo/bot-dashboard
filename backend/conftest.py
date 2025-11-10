import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
os.environ.setdefault('USE_SQLITE', 'true')
django.setup()
