from django.shortcuts import render

from catalog.models import Gift, Brand, GiftInstance, Category

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_gifts = Gift.objects.all().count()
    num_instances = GiftInstance.objects.all().count()

    # Available gifts (status = 'a')
    num_instances_available = GiftInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_brands = Brand.objects.count()

    context = {
        'num_gifts': num_gifts,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_brands': num_brands,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
