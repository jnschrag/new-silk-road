from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from publish.views import PublicationMixin

from .models import (
    Person,
    Organization,
    Event,
)


class PersonDetailView(PublicationMixin, DetailView):
    model = Person
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'


class PersonListView(PublicationMixin, ListView):
    model = Person
    paginate_by = 50


class EventDetailView(PublicationMixin, DetailView):
    model = Event


class EventListView(PublicationMixin, ListView):
    model = Event
    paginate_by = 50


# Organization stuff
class OrganizationDetailView(PublicationMixin, DetailView):
    queryset = Organization.publishable_objects.all()
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'


class OrganizationListView(PublicationMixin, ListView):
    queryset = Organization.publishable_objects.all()
    paginate_by = 50
    display_name_plural = None

    def get_context_data(self, **kwargs):
        context = super(OrganizationListView, self).get_context_data(**kwargs)
        if hasattr(self, 'display_name_plural'):
            context['display_name_plural'] = self.display_name_plural
        return context


class OrganizationListRedirectView(RedirectView):
    permanent = True
    pattern_name = None

    def get_redirect_url(self, *args, **kwargs):
        org_type = kwargs.pop('org_type', None)
        if org_type:
            self.pattern_name = 'facts:{}-list'.format(org_type.lower())
        return super().get_redirect_url(*args, **kwargs)


class CompanyListView(OrganizationListView):
    queryset = Organization.objects.filter(companydetails__isnull=False)
    display_name_plural = 'Companies'


class FinancingOrganizationListView(OrganizationListView):
    queryset = Organization.objects.filter(financingorganizationdetails__isnull=False)
    display_name_plural = 'Financing Organizations'


class GovernmentListView(OrganizationListView):
    queryset = Organization.objects.filter(governmentdetails__isnull=False)
    display_name_plural = 'Governments'


class MilitaryListView(OrganizationListView):
    queryset = Organization.objects.filter(militarydetails__isnull=False)
    display_name_plural = 'Militaries'


class MultilateralListView(OrganizationListView):
    queryset = Organization.objects.filter(multilateraldetails__isnull=False)
    display_name_plural = 'Multilaterals'


class NGOListView(OrganizationListView):
    queryset = Organization.objects.filter(ngodetails__isnull=False)
    display_name_plural = 'Non-governmental organizations'


class PoliticalListView(OrganizationListView):
    queryset = Organization.objects.filter(politicaldetails__isnull=False)
    display_name_plural = 'Politcal Entities'
