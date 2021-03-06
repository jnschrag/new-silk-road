from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from publish.models import Publishable
from publish.models import PublishableQuerySet
from markymark.fields import MarkdownField
from markymark.utils import render_markdown
from mptt.models import MPTTModel, TreeForeignKey
from finance.credit import (MOODYS_LONG_TERM,
                            STANDARD_POORS_LONG_TERM,
                            FITCH_LONG_TERM)
from utilities.date import fuzzydate
import uuid

DETAIL_MODEL_NAMES = {
    'companydetails': 'Company',
    'financingorganizationdetails': 'Financing Organization',
    'governmentdetails': 'Government',
    'militarydetails': 'Military',
    'multilateraldetails': 'Multilateral',
    'ngodetails': 'NGO',
    'politicaldetails': 'Political Entity',
}


class Organization(MPTTModel, Publishable):
    """Abstract base model for organizations"""

    identifier = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, allow_unicode=True)
    countries = models.ManyToManyField('locations.Country', blank=True)
    leaders = models.ManyToManyField('Person', blank=True,
                                     related_name='organizations_led')
    initiatives = models.ManyToManyField('infrastructure.Initiative', blank=True)
    headquarters = models.ForeignKey('locations.Place', models.SET_NULL, blank=True, null=True)

    description = MarkdownField(blank=True)
    description_rendered = models.TextField(blank=True, editable=False)

    notes = MarkdownField(blank=True)
    related_events = models.ManyToManyField('Event', blank=True)
    founding_year = models.PositiveSmallIntegerField(blank=True, null=True)
    founding_month = models.PositiveSmallIntegerField(blank=True, null=True)
    founding_day = models.PositiveSmallIntegerField(blank=True, null=True)

    @property
    def fuzzy_founding_date(self):
        return fuzzydate(self.founding_year, self.founding_month, self.founding_day)

    dissolution_year = models.PositiveSmallIntegerField(blank=True, null=True)
    dissolution_month = models.PositiveSmallIntegerField(blank=True, null=True)
    dissolution_day = models.PositiveSmallIntegerField(blank=True, null=True)

    @property
    def fuzzy_dissolution_date(self):
        return fuzzydate(self.dissolution_year, self.dissolution_month, self.dissolution_day)

    parent = TreeForeignKey('self', null=True, blank=True,
                            verbose_name='parent organization',
                            related_name='children', db_index=True)
    staff_size = models.PositiveIntegerField("Staff/Personnel count",
                                             blank=True, null=True)
    mission = MarkdownField("Mandate/Mission Statement", blank=True)
    mission_rendered = models.TextField(blank=True, editable=False)
    related_organizations = models.ManyToManyField('self', blank=True)

    documents = models.ManyToManyField('sources.Document', blank=True)

    publishable_objects = PublishableQuerySet.as_manager()

    class MPTTMeta:
            order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = "all organizations"
        ordering = ['name', 'created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('facts:organization-detail', kwargs={
            'slug': self.slug,
            'identifier': str(self.identifier)
        })

    def get_detail_types(self):
        return {
            model_name: label
            for model_name, label in DETAIL_MODEL_NAMES.items()
            if hasattr(self, model_name)
        }

    def get_organization_types(self):
        return frozenset([
            label
            for model_name, label in DETAIL_MODEL_NAMES.items()
            if hasattr(self, model_name)
        ])

    def save(self, *args, **kwargs):
        self.description_rendered = render_markdown(self.description)
        self.mission_rendered = render_markdown(self.mission)
        if not self.slug or self.slug == '':
            self.slug = slugify(self.name, allow_unicode=True)
        super(Organization, self).save(*args, **kwargs)


class OrganizationTypeBase(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, allow_unicode=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = slugify(self.name, allow_unicode=True)
        super(OrganizationTypeBase, self).save(*args, **kwargs)


class CompanyType(MPTTModel, OrganizationTypeBase):
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)


class FinancingType(MPTTModel, OrganizationTypeBase):
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)


class MultilateralType(MPTTModel, OrganizationTypeBase):
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)


class NGOType(MPTTModel, OrganizationTypeBase):
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)

    class Meta:
        verbose_name = "NGO type"


class PoliticalType(MPTTModel, OrganizationTypeBase):
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)


class CompanyStructure(models.Model):
    """Describes structure of a company"""
    name = models.CharField("Structure", max_length=100)
    slug = models.SlugField(max_length=110, allow_unicode=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = slugify(self.name, allow_unicode=True)
        super(CompanyStructure, self).save(*args, **kwargs)


# Details
class OrganizationDetails(models.Model):
    organization = models.OneToOneField(
        'facts.Organization',
        models.CASCADE
    )

    class Meta:
        abstract = True

    def __str__(self):
        return "{} for {}".format(
            self._meta.verbose_name.title(),
            self.organization.name
        )


class CompanySector(object):
    SECTOR_PRIMARY = 1
    SECTOR_SECONDARY = 2
    SECTOR_TERTIARY = 3

    CHOICES = (
        (SECTOR_PRIMARY, "Primary (raw materials)"),
        (SECTOR_SECONDARY, "Secondary (manufacturing)"),
        (SECTOR_TERTIARY, "Tertiary (sales and services)"),
    )

    @classmethod
    def get_label_for_sector(cls, value):
        return dict(CompanySector.CHOICES).get(value, "")


class CompanyDetails(OrganizationDetails):
    """Details of an company"""

    structure = models.ForeignKey('facts.CompanyStructure', models.SET_NULL, blank=True, null=True)
    sectors = ArrayField(
        models.PositiveSmallIntegerField(blank=True, null=True, choices=CompanySector.CHOICES),
        blank=True,
        default=list
    )
    org_type = models.ForeignKey('facts.CompanyType',
                                 models.SET_NULL, blank=True, null=True,
                                 verbose_name='type')

    def get_sector_list_display(self):
        return ','.join((CompanySector.get_label_for_sector(x) for x in self.sectors if x))

    class Meta:
        verbose_name_plural = "company details"


class FinancingOrganizationDetails(OrganizationDetails):
    """Details of a financing organization"""

    MOODYS_RATING_CHOICES = tuple(x for x in enumerate(MOODYS_LONG_TERM, start=1))
    FITCH_RATING_CHOICES = tuple(x for x in enumerate(FITCH_LONG_TERM, start=101))
    STANDARD_POORS_RATING_CHOICES = tuple(x for x in enumerate(STANDARD_POORS_LONG_TERM, start=201))

    # Financials
    approved_capital = models.DecimalField(blank=True, null=True,
                                           max_digits=17, decimal_places=2)
    moodys_credit_rating = models.PositiveSmallIntegerField(
        choices=MOODYS_RATING_CHOICES, blank=True, null=True
    )
    fitch_credit_rating = models.PositiveSmallIntegerField(
        choices=FITCH_RATING_CHOICES, blank=True, null=True
    )
    sp_credit_rating = models.PositiveSmallIntegerField(
        "Standard & Poors Credit Rating",
        choices=STANDARD_POORS_RATING_CHOICES, blank=True, null=True
    )
    shareholder_organizations = models.ManyToManyField('facts.Organization',
                                                       related_name='holds_shares_of',
                                                       through='OrganizationShareholder')
    shareholder_people = models.ManyToManyField('facts.Person',
                                                related_name='holds_shares_of',
                                                through='PersonShareholder')
    scope_of_operations = models.ManyToManyField('locations.Place', blank=True)
    procurement = models.CharField(blank=True, max_length=100)
    org_type = models.ForeignKey('facts.FinancingType',
                                 models.SET_NULL, blank=True, null=True,
                                 verbose_name='type')
    members = models.ManyToManyField(
        'Organization',
        related_name='financingorganization_memberships',
        blank=True,
    )

    def get_credit_ratings_display(self):
        return (
            self.get_moodys_credit_rating_display(),
            self.get_fitch_credit_rating_display(),
            self.get_sp_credit_rating_display()
        )

    class Meta:
        verbose_name_plural = "financing organization details"


class GovernmentDetails(OrganizationDetails):
    """Details of a government"""
    country = models.ForeignKey('locations.Country', models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = "government details"


class MilitaryDetails(OrganizationDetails):
    """Details of a military variable"""
    country = models.ForeignKey('locations.Country', models.SET_NULL, blank=True, null=True)
    ruling_party = models.BooleanField(default=True)
    budget = models.DecimalField(blank=True, null=True,
                                 max_digits=17, decimal_places=2)

    class Meta:
        verbose_name_plural = "military details"


class MultilateralDetails(OrganizationDetails):
    """Details of a multilateral organization"""
    members = models.ManyToManyField('Organization',
                                     related_name='multilateral_memberships'
                                     )
    org_type = models.ForeignKey('MultilateralType',
                                 models.SET_NULL, blank=True, null=True,
                                 verbose_name='type')

    class Meta:
        verbose_name_plural = "multilateral details"


class NGODetails(OrganizationDetails):
    """Details of an NGO (Non-governmental Organization)"""
    members = models.ManyToManyField('Organization',
                                     related_name='ngo_memberships'
                                     )
    geographic_scope = models.ManyToManyField(
        'locations.Place',
        blank=True,
        help_text='Geographic scope as defined by a selection of Place records.'
    )
    endowment = models.DecimalField(blank=True, null=True,
                                    max_digits=17, decimal_places=2)
    org_type = models.ForeignKey('NGOType',
                                 models.SET_NULL, blank=True, null=True,
                                 verbose_name='type')

    class Meta:
        verbose_name_plural = "NGO details"


class PoliticalDetails(OrganizationDetails):
    """Details of a Political Entity"""
    countries = models.ManyToManyField('locations.Country', blank=True)
    org_type = models.ForeignKey('PoliticalType',
                                 models.SET_NULL, blank=True, null=True,
                                 verbose_name='type')
    ruling_party = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "poltitical details"


# Shareholders

class ShareholderBase(models.Model):
    investment = models.ForeignKey(
        'facts.FinancingOrganizationDetails',
        on_delete=models.CASCADE
    )
    value = models.DecimalField('% Share', max_digits=5, decimal_places=2)

    class Meta:
        abstract = True
        ordering = ['investment', '-value']


class OrganizationShareholder(ShareholderBase):
    shareholder = models.ForeignKey(
        'facts.Organization',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}: {}%".format(self.shareholder, self.value)


class PersonShareholder(ShareholderBase):
    shareholder = models.ForeignKey(
        'facts.Person',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}: {}%".format(self.shareholder, self.value)
