import rest_framework_filters as filters
from rest_framework_gis.filterset import GeoFilterSet
from locations.models import (
    LineStringGeometry,
    PointGeometry,
    PolygonGeometry,
    GeometryStore,

    Country,
    Region
)


class GeometryStoreFilter(GeoFilterSet):
    name = filters.CharFilter(name='attributes__name', lookup_expr='iexact')
    name__contains = filters.CharFilter(name='attributes__name', lookup_expr='icontains')

    class Meta:
        model = GeometryStore
        fields = ('identifier',)


def filter_region_json(qs, value):
    return qs.filter(attributes__region=int(value))


def filter_json_has_key(qs, value):
    return qs.filter(attributes__has_key=value)


class LocationGeometryFilterBase(GeoFilterSet):
    label = filters.CharFilter(name='label', lookup_expr='iexact')
    label__contains = filters.CharFilter(name='label', lookup_expr='icontains')

    name = filters.CharFilter(name='attributes__name', lookup_expr='exact')
    layer = filters.CharFilter(name='attributes__layer', lookup_expr='exact')
    region = filters.NumberFilter(name='attributes__region', action=filter_region_json)
    # FIXME: has_key/filter_json_has_key messes up all queries.
    # has_key = filters.CharFilter(name='attributes', action=filter_json_has_key)


class LineStringGeometryFilter(LocationGeometryFilterBase):
    class Meta:
        model = LineStringGeometry


class PointGeometryFilter(LocationGeometryFilterBase):
    class Meta:
        model = PointGeometry


class PolygonGeometryFilter(LocationGeometryFilterBase):
    class Meta:
        model = PolygonGeometry


class CountryFilter(filters.FilterSet):
    name = filters.AllLookupsFilter(name='name')
    code = filters.AllLookupsFilter(name='alpha_3')

    class Meta:
        model = Country
        fields = ['name', 'code']


class RegionFilter(filters.FilterSet):
    name = filters.AllLookupsFilter(name='name')

    class Meta:
        model = Region
        fields = ['name']
