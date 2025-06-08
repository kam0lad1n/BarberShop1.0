# yourapp/context_processors.py
from .models import Site

def site_data(request):
    return {
        'site': Site.objects.first()
    }
