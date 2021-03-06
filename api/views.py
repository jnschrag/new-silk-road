from django.db.models import Count
from django.conf import settings
from rest_framework import viewsets, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_gis.filters import InBBoxFilter

from locations.models import (
    LineStringGeometry,
    PointGeometry,
    PolygonGeometry,
    GeometryStore,
    Region,
    Country
)
from api.serializers.locations import (
    LineStringGeometrySerializer,
    PointGeometrySerializer,
    PolygonGeometrySerializer,
    GeometryStoreDetailSerializer,
    GeometryStoreCentroidSerializer,
    RegionBasicSerializer,
    CountryBasicSerializer
)
from api.filters.locations import (
    GeometryStoreFilter,
    LineStringGeometryFilter,
    PointGeometryFilter,
    PolygonGeometryFilter

)
from infrastructure.models import (
    Project,
    ProjectStatus,
    Initiative,
    InfrastructureType
)
from facts.models import (
    Organization
)
from api.serializers.infrastructure import (ProjectSerializer, InitiativeSerializer, InfrastructureTypeSerializer)
from api.serializers.facts import (OrganizationBasicSerializer)
from api.filters.infrastructure import (ProjectFilter, InitiativeFilter)
from api.filters.facts import (OrganizationFilter)
from publish.views import PublicationMixin

PUBLISH_FILTER_ENABLED = getattr(settings, 'PUBLISH_FILTER_ENABLED', True)


class OrganizationViewSet(PublicationMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.distinct().all()
    lookup_field = 'identifier'
    serializer_class = OrganizationBasicSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = OrganizationFilter


class ProjectViewSet(PublicationMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.distinct().select_related(
        'infrastructure_type',
    ).all()
    lookup_field = 'identifier'
    serializer_class = ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProjectFilter


class InitiativeViewSet(PublicationMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Initiative.objects.distinct().all()
    lookup_field = 'identifier'
    serializer_class = InitiativeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = InitiativeFilter


class InfrastructureTypeListView(generics.ListAPIView):
    queryset = InfrastructureType.objects.distinct().all()
    serializer_class = InfrastructureTypeSerializer
    pagination_class = None


class ProjectStatusListView(APIView):
    def get(self, request, format=None):
        statuses = [{'id': s[0], 'name': s[1]} for s in ProjectStatus.STATUSES]
        return Response(statuses)


# locations
class LineStringGeometryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LineStringGeometry.objects.distinct().all()
    serializer_class = LineStringGeometrySerializer
    bbox_filter_field = 'geom'
    filter_backends = (InBBoxFilter, filters.DjangoFilterBackend)
    filter_class = LineStringGeometryFilter


class PointGeometryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PointGeometry.objects.distinct().all()
    serializer_class = PointGeometrySerializer
    bbox_filter_field = 'geom'
    filter_backends = (InBBoxFilter, filters.DjangoFilterBackend)
    filter_class = PointGeometryFilter


class PolygonGeometryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PolygonGeometry.objects.distinct().all()
    serializer_class = PolygonGeometrySerializer
    bbox_filter_field = 'geom'
    filter_backends = (InBBoxFilter, filters.DjangoFilterBackend)
    filter_class = PolygonGeometryFilter


class GeometryStoreDetailView(generics.RetrieveAPIView):
    lookup_field = 'identifier'
    serializer_class = GeometryStoreDetailSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = GeometryStoreFilter

    def get_queryset(self):
        queryset = GeometryStore.objects\
            .annotate(num_projects=Count('projects'))\
            .filter(num_projects__gt=0)

        if PUBLISH_FILTER_ENABLED and not self.request.user.is_authenticated():
            queryset = queryset.filter(projects__published=True).distinct()

        return queryset


class GeometryStoreCentroidViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'identifier'
    serializer_class = GeometryStoreCentroidSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = GeometryStoreFilter
    pagination_class = None

    def get_queryset(self):
        queryset = GeometryStore.objects\
            .exclude(lines=None, points=None, polygons=None)\
            .exclude(centroid__isnull=True)\
            .annotate(num_projects=Count('projects'))\
            .filter(num_projects__gt=0)

        if PUBLISH_FILTER_ENABLED and not self.request.user.is_authenticated():
            queryset = queryset.filter(projects__published=True).distinct()

        return queryset


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.distinct().all()
    serializer_class = RegionBasicSerializer
    pagination_class = None


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.distinct().all()
    serializer_class = CountryBasicSerializer
    pagination_class = None
