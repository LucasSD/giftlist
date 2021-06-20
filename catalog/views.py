from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from catalog.models import Brand, Category, Gift, GiftInstance


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_gifts = Gift.objects.all().count()
    num_instances = GiftInstance.objects.all().count()

    # Available gifts (status = 'a')
    num_instances_available = GiftInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_brands = Brand.objects.count()

    # session info
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # random challenge
    num_perfume_gifts = Gift.objects.filter(description__icontains='Perfume').count()
    num_older_brands = Brand.objects.exclude(est__gt=1999).count()

    context = {
        'num_gifts': num_gifts,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_brands': num_brands,
        'num_perfume_gifts': num_perfume_gifts,
        'num_older_brands': num_older_brands,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class GiftListView(generic.ListView):
    model = Gift
    paginate_by = 3

class GiftDetailView(generic.DetailView):
    model = Gift

class BrandListView(generic.ListView):
    model = Brand
    paginate_by = 2

class BrandDetailView(generic.DetailView):
    model = Brand

class GiftInstanceListView(LoginRequiredMixin, generic.ListView):
    model = GiftInstance
    paginate_by = 3

    def get_queryset(self):
        """Override to return GiftInstance objects uploaded by current user.
        Returns:
            QuerySet: A list of GiftInstance objects.
        """

        return GiftInstance.objects.filter(requester=self.request.user).order_by('event_date')

# add login mixin
class GiftInstanceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = GiftInstance
    fields = ["event_date", "size", "colour", "price", "url", "requester"]
    success_url = reverse_lazy("mygifts")
