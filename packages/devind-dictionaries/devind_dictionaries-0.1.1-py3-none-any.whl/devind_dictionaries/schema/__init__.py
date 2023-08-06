"""Description schema for dictionaries.

Last change: Luferov
Time: 2022-03-2
"""

from typing import Any

import graphene
from devind_helpers.orm_utils import get_object_or_404
from graphene_django import DjangoListField
from graphene_django_filter import AdvancedDjangoFilterConnectionField
from graphql import ResolveInfo

from .mutations import UpdateOrganizations
from .types import DistrictType, OrganizationType, RegionType
from ..models import District, Organization, Region


class Query(graphene.ObjectType):
    """List of queries for dictionaries."""

    district = graphene.Field(DistrictType, district_id=graphene.Int(required=True, description='District ID'))
    districts = DjangoListField(DistrictType)

    region = graphene.Field(RegionType, region_id=graphene.Int(required=True, description='Region ID'))
    regions = DjangoListField(RegionType)

    organization = graphene.Field(
        OrganizationType,
        organization_id=graphene.Int(required=True, description='Organization ID')
    )
    organizations = AdvancedDjangoFilterConnectionField(OrganizationType)

    @staticmethod
    def resolve_district(root: Any, info: ResolveInfo, district_id: int) -> District:
        """Resolve get district entity."""
        return get_object_or_404(District, pk=district_id)

    @staticmethod
    def resolve_region(root: Any, info: ResolveInfo, region_id: int) -> Region:
        """Resolve get region entity."""
        return get_object_or_404(Region, pk=region_id)

    @staticmethod
    def resolve_organization(root: Any, info: ResolveInfo, organization_id: int) -> Organization:
        """Resolve get organizations entiry."""
        return get_object_or_404(Organization, pk=organization_id)


class Mutation(graphene.ObjectType):
    """List of mutations for dictionaries."""

    update_organizations = UpdateOrganizations.Field(description='Update district, regions and organizations.')
