"""Graphql Types for dictionaries."""

import graphene
from devind_helpers.optimized import OptimizedDjangoObjectType
from graphene_django import DjangoObjectType

from ..filters import DistrictFilter, OrganizationFilter, RegionFilter
from ..models import District, Organization, Region


class DistrictType(DjangoObjectType):
    """Optimized type for District."""

    class Meta:
        """Metaclass with description parameters."""

        model = District
        fields = ('id', 'name', 'created_at', 'updated_at',)
        filterset_class = DistrictFilter


class RegionType(DjangoObjectType):
    """Optimized type for Regions."""

    class Meta:
        """Metaclass with description parameters."""

        model = Region
        fields = ('id', 'name', 'common_id', 'created_at', 'updated_at',)
        filterset_class = RegionFilter


class OrganizationType(OptimizedDjangoObjectType):
    """Optimized type for Organizations."""

    class Meta:
        """Metaclass with description parameters."""

        model = Organization
        interfaces = (graphene.relay.Node,)
        fields = (
            'name', 'present_name',
            'inn', 'kpp', 'kind',
            'rubpnubp', 'kodbuhg', 'okpo',
            'phone', 'site', 'mail', 'address',
            'attributes',
            'created_at', 'updated_at',
            'parent',
            'region',
        )
        filterset_class = OrganizationFilter
