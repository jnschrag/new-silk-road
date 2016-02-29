from django.db import models
from django.contrib.postgres.fields import ArrayField
from publish.models import Publishable
from markymark.fields import MarkdownField
from mptt.models import MPTTModel, TreeForeignKey
from .locations import COUNTRY_CHOICES


class OrganizationTypeBase(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True


class FinancingType(MPTTModel, OrganizationTypeBase):
    pass


class CompanyType(MPTTModel, OrganizationTypeBase):
    pass


class MultilateralType(MPTTModel, OrganizationTypeBase):
    pass


class NGOType(MPTTModel, OrganizationTypeBase):
    pass


class PoliticalType(MPTTModel, OrganizationTypeBase):
    pass


class Organization(MPTTModel, Publishable):
    """Abstract base model for organizations"""
    name = models.CharField(max_length=100)
    leaders = models.ManyToManyField('Person', related_name='organizations_led')
    initiatives = models.ManyToManyField('Initiative')
    headquarters = models.ForeignKey('Place')
    notes = MarkdownField(blank=True, help_text='Notes for display on website')
    founding_date = models.DateField(blank=True, null=True)
    dissolution_date = models.DateField(blank=True, null=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)
    affiliated_organizations = models.ManyToManyField('self')
    staff_size = models.PositiveSmallIntegerField("Staff/Personel count",
                                                  blank=True, null=True)
    mission = models.TextField("Mandate/Mission Statement", blank=True)

    def __str__(self):
        return self.name


class Government(Organization):
    """Describes a government"""
    country = models.PositiveSmallIntegerField(choices=COUNTRY_CHOICES, blank=True, null=True)


class FinancingOrganization(Organization):
    """Describes a financing organization"""
    # Relations
    related_forgs = models.ManyToManyField('self',
                                           verbose_name="affiliated financing organizations")
    related_companies = models.ManyToManyField('Company')
    related_governments = models.ManyToManyField('Government')
    # Financials
    approved_capital = models.DecimalField(max_digits=17, decimal_places=2)
    credit_rating = models.CharField(blank=True, max_length=100)
    # shareholders = ???
    scope_of_operations = models.CharField(blank=True, max_length=100)
    procurement = models.CharField(blank=True, max_length=100)
    org_type = models.ForeignKey('FinancingType', verbose_name='type')


class CompanyStructure(models.Model):
    """Describes structure of a company"""
    name = models.CharField("Structure", max_length=100)


class Company(Organization):
    """Describes an company"""

    SECTOR_PRIMARY = 1
    SECTOR_SECONDARY = 2
    SECTOR_TERTIARY = 3

    SECTOR_CHOICES = (
        (SECTOR_PRIMARY, "Primary"),
        (SECTOR_SECONDARY, "Secondary"),
        (SECTOR_TERTIARY, "Tertiary"),
    )

    related_forgs = models.ManyToManyField('self',
                                           verbose_name="affiliated financing organizations")
    related_companies = models.ManyToManyField('Company')
    related_governments = models.ManyToManyField('Government')
    structure = models.ForeignKey('CompanyStructure')
    sector = models.PositiveSmallIntegerField(blank=True, null=True, choices=SECTOR_CHOICES)
    org_type = models.ForeignKey('CompanyType', verbose_name='type')


class Multilateral(Organization):
    """Describes a multilateral organization"""
    # members = ???
    org_type = models.ForeignKey('MultilateralType', verbose_name='type')


class NonGovernmental(Organization):
    """Describes an NGO"""
    related_events = models.ManyToManyField('Event')
    # members = ???
    # geographic_scope = ???
    endowment = models.DecimalField(max_digits=17, decimal_places=2)
    org_type = models.ForeignKey('NGOType', verbose_name='type')

    class Meta:
        verbose_name = "ngo"


class Political(Organization):
    """Describes a Political Entity"""
    countries = ArrayField(
        models.PositiveSmallIntegerField(choices=COUNTRY_CHOICES, blank=True, null=True),
        blank=True, null=True, default=list
    )
    org_type = models.ForeignKey('PoliticalType', verbose_name='type')
    ruling_party = models.BooleanField(default=True)


class Military(Organization):
    """Describes a military variable"""
    country = models.PositiveSmallIntegerField(choices=COUNTRY_CHOICES, blank=True, null=True)
    ruling_party = models.BooleanField(default=True)
    budget = models.DecimalField(max_digits=17, decimal_places=2)
    related_events = models.ManyToManyField('Event')
