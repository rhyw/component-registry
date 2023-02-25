import json
import logging
from typing import Type, Union

import django_filters.rest_framework
from django.db import connections
from django.db.models import QuerySet, Value
from django.http import Http404
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from mptt.templatetags.mptt_tags import cache_tree_children
from packageurl import PackageURL
from rest_framework import filters, status
from rest_framework.decorators import action, api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from config import utils
from corgi import __version__
from corgi.core.models import (
    AppStreamLifeCycle,
    Channel,
    Component,
    ComponentNode,
    Product,
    ProductStream,
    ProductVariant,
    ProductVersion,
    SoftwareBuild,
)

from .constants import CORGI_API_VERSION
from .filters import (
    ChannelFilter,
    ComponentFilter,
    ProductDataFilter,
    SoftwareBuildFilter,
)
from .serializers import (
    AppStreamLifeCycleSerializer,
    ChannelSerializer,
    ComponentListSerializer,
    ComponentProductStreamSummarySerializer,
    ComponentSerializer,
    ProductSerializer,
    ProductStreamSerializer,
    ProductStreamSummarySerializer,
    ProductVariantSerializer,
    ProductVersionSerializer,
    SoftwareBuildSerializer,
    get_component_purl_link,
    get_model_ofuri_type,
)

logger = logging.getLogger(__name__)

INCLUDE_FIELDS_PARAMETER = OpenApiParameter(
    "include_fields",
    type={"type": "array", "items": {"type": "string"}},
    location=OpenApiParameter.QUERY,
    description=(
        "Include only specified fields in the response. "
        "Multiple values may be separated by commas. "
        "Example: `include_fields=software_build.build_id,name`"
    ),
)

EXCLUDE_FIELDS_PARAMETER = OpenApiParameter(
    "exclude_fields",
    type={"type": "array", "items": {"type": "string"}},
    location=OpenApiParameter.QUERY,
    description=(
        "Exclude only specified fields in the response. "
        "Multiple values may be separated by commas. "
        "Example: `exclude_fields=software_build.build_id,name`"
    ),
)


# Use below as a decorator on all viewsets that support
# ?include_fields&exclude_fields= parameters
# A custom IncludeExcludeFieldsViewSet class that other
# ViewSet classes inherit from does not work
INCLUDE_EXCLUDE_FIELDS_SCHEMA = extend_schema_view(
    list=extend_schema(
        parameters=[INCLUDE_FIELDS_PARAMETER, EXCLUDE_FIELDS_PARAMETER],
    ),
    retrieve=extend_schema(
        parameters=[INCLUDE_FIELDS_PARAMETER, EXCLUDE_FIELDS_PARAMETER],
    ),
)


@extend_schema(request=None, responses=None)
@api_view(["GET"])
def healthy(request: Request) -> Response:
    """Send empty 200 response as an indicator that the application is up and running."""
    return Response(status=status.HTTP_200_OK)


class StatusViewSet(GenericViewSet):
    # Note-including a dummy queryset as scheme generation is complaining for reasons unknown
    queryset = Product.objects.none()

    @extend_schema(
        request=None,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "dt": {"type": "string", "format": "date-time"},
                    "service_version": {"type": "string"},
                    "rest_api_version": {"type": "string"},
                    "db_size": {"type": "string"},
                    "builds": {
                        "type": "object",
                        "properties": {"count": {"type": "integer"}},
                    },
                    "products": {
                        "type": "object",
                        "properties": {"count": {"type": "integer"}},
                    },
                    "product_versions": {
                        "type": "object",
                        "properties": {"count": {"type": "integer"}},
                    },
                    "product_streams": {
                        "type": "object",
                        "properties": {"count": {"type": "integer"}},
                    },
                    "product_variants": {
                        "type": "object",
                        "properties": {"count": {"type": "integer"}},
                    },
                    "channels": {
                        "type": "object",
                        "properties": {"count": {"type": "integer"}},
                    },
                    "components": {
                        "type": "object",
                        "properties": {"count": {"type": "integer"}},
                    },
                    "relations": {
                        "type": "object",
                        "properties": {"count": {"type": "integer"}},
                    },
                },
            }
        },
    )
    def list(self, request: Request) -> Response:
        # pg has well known limitation with counting
        #        (https://wiki.postgresql.org/wiki/Slow_Counting)
        # the following approach provides an estimate for raw table counts which performs
        # much better.
        with connections["read_only"].cursor() as cursor:
            cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()));")
            db_size = cursor.fetchone()
            cursor.execute(
                "SELECT reltuples AS estimate FROM pg_class "
                "WHERE relname = 'core_productcomponentrelation';"
            )
            pcr_count = cursor.fetchone()
            cursor.execute(
                "SELECT reltuples AS estimate FROM pg_class WHERE relname = 'core_component';"
            )
            component_count = cursor.fetchone()
            cursor.execute(
                "SELECT reltuples AS estimate FROM pg_class WHERE relname = 'core_softwarebuild';"
            )
            sb_count = cursor.fetchone()

        return Response(
            {
                "status": "ok",
                "dt": timezone.now(),
                "service_version": __version__,
                "rest_api_version": CORGI_API_VERSION,
                "db_size": db_size,
                "builds": {
                    "count": sb_count,
                },
                "components": {
                    "count": component_count,
                },
                "relations": {"count": pcr_count},
                "products": {
                    "count": Product.objects.db_manager("read_only").count(),
                },
                "product_versions": {
                    "count": ProductVersion.objects.db_manager("read_only").count(),
                },
                "product_streams": {
                    "count": ProductStream.objects.db_manager("read_only").count(),
                },
                "product_variants": {
                    "count": ProductVariant.objects.db_manager("read_only").count(),
                },
                "channels": {
                    "count": Channel.objects.db_manager("read_only").count(),
                },
            }
        )


# A dict with string keys and string or tuple values
# The tuples recursively contain taxonomy dicts
taxonomy_dict_type = dict[str, Union[str, tuple["taxonomy_dict_type", ...]]]


def recursive_component_node_to_dict(
    node: ComponentNode, component_type: tuple[str, ...]
) -> taxonomy_dict_type:
    """Recursively build a dict of purls, links, and children for some ComponentNode"""
    if not node.obj:
        raise ValueError(f"Node {node} had no linked obj")

    result = {}
    if node.type in component_type:
        result = {
            "purl": node.purl,
            # "node_id": node.pk,
            "node_type": node.type,
            "link": get_component_purl_link(node.purl),
            # "uuid": node.obj.uuid,
            "description": node.obj.description,
        }
    children = tuple(
        recursive_component_node_to_dict(c, component_type) for c in node.get_children()
    )
    if children:
        result["deps"] = children
    return result


def get_component_taxonomy(
    obj: Component, component_types: tuple[str, ...]
) -> tuple[taxonomy_dict_type, ...]:
    """Look up and return the taxonomy for a particular Component."""
    root_nodes = cache_tree_children(
        obj.cnodes.get_queryset().get_descendants(include_self=True).using("read_only")
    )
    dicts = tuple(
        recursive_component_node_to_dict(
            node,
            component_types,
        )
        for node in root_nodes
    )
    return dicts


@INCLUDE_EXCLUDE_FIELDS_SCHEMA
class SoftwareBuildViewSet(ReadOnlyModelViewSet):  # TODO: TagViewMixin disabled until auth is added
    """View for api/v1/builds"""

    queryset = SoftwareBuild.objects.order_by("-build_id").using("read_only")
    serializer_class = SoftwareBuildSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = SoftwareBuildFilter
    lookup_url_kwarg = "build_id"


class ProductDataViewSet(ReadOnlyModelViewSet):  # TODO: TagViewMixin disabled until auth is added
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "description", "meta_attr"]
    filterset_class = ProductDataFilter
    lookup_url_kwarg = "uuid"
    ordering_field = "name"


@INCLUDE_EXCLUDE_FIELDS_SCHEMA
class ProductViewSet(ProductDataViewSet):
    """View for api/v1/products"""

    # Can't use self / super() yet
    queryset = Product.objects.order_by(ProductDataViewSet.ordering_field).using("read_only")
    serializer_class = ProductSerializer

    def list(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        req = self.request
        ofuri = req.query_params.get("ofuri")
        if not ofuri:
            return super().list(request)
        return super().retrieve(request)

    def get_object(self):
        req = self.request
        p_ofuri = req.query_params.get("ofuri")
        p_name = req.query_params.get("name")
        try:
            if p_name:
                p = Product.objects.db_manager("read_only").get(name=p_name)
            elif p_ofuri:
                p = Product.objects.db_manager("read_only").get(ofuri=p_ofuri)
            else:
                pk = req.path.split("/")[-1]  # there must be better ways ...
                p = Product.objects.db_manager("read_only").get(uuid=pk)
            return p
        except Product.DoesNotExist:
            raise Http404


@INCLUDE_EXCLUDE_FIELDS_SCHEMA
class ProductVersionViewSet(ProductDataViewSet):
    """View for api/v1/product_versions"""

    queryset = ProductVersion.objects.order_by(ProductDataViewSet.ordering_field).using("read_only")
    serializer_class = ProductVersionSerializer

    def list(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        req = self.request
        ofuri = req.query_params.get("ofuri")
        if not ofuri:
            return super().list(request)
        return super().retrieve(request)

    def get_object(self):
        req = self.request
        pv_ofuri = req.query_params.get("ofuri")
        pv_name = req.query_params.get("name")
        try:
            if pv_name:
                pv = ProductVersion.objects.db_manager("read_only").get(name=pv_name)
            elif pv_ofuri:
                pv = ProductVersion.objects.db_manager("read_only").get(ofuri=pv_ofuri)
            else:
                pk = req.path.split("/")[-1]  # there must be better ways ...
                pv = ProductVersion.objects.db_manager("read_only").get(uuid=pk)
            return pv
        except ProductVersion.DoesNotExist:
            raise Http404


@INCLUDE_EXCLUDE_FIELDS_SCHEMA
class ProductStreamViewSetSet(ProductDataViewSet):
    """View for api/v1/product_streams"""

    queryset = (
        ProductStream.objects.filter(active=True)
        .order_by(ProductDataViewSet.ordering_field)
        .using("read_only")
    )
    serializer_class: Union[
        Type[ProductStreamSerializer], Type[ProductStreamSummarySerializer]
    ] = ProductStreamSerializer

    @extend_schema(
        parameters=[OpenApiParameter("active", OpenApiTypes.STR, OpenApiParameter.QUERY)]
    )
    def list(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        view = request.query_params.get("view")
        ps_ofuri = request.query_params.get("ofuri")
        ps_name = request.query_params.get("name")
        active = request.query_params.get("active")
        if active == "all":
            self.queryset = ProductStream.objects.order_by(super().ordering_field).using(
                "read_only"
            )
        if not ps_ofuri and not ps_name:
            if view == "summary":
                self.serializer_class = ProductStreamSummarySerializer
            return super().list(request)
        return super().retrieve(request)

    def get_object(self):
        req = self.request
        ps_ofuri = req.query_params.get("ofuri")
        ps_name = req.query_params.get("name")
        try:
            if ps_name:
                ps = ProductStream.objects.db_manager("read_only").get(name=ps_name)
            elif ps_ofuri:
                ps = ProductStream.objects.db_manager("read_only").get(ofuri=ps_ofuri)
            else:
                pk = req.path.split("/")[-1]  # there must be better ways ...
                ps = ProductStream.objects.db_manager("read_only").get(uuid=pk)
            return ps
        except ProductStream.DoesNotExist:
            raise Http404

    @action(methods=["get"], detail=True)
    def manifest(self, request: Request, uuid: Union[str, None] = None) -> Response:
        obj = self.queryset.filter(uuid=uuid).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        manifest = json.loads(obj.manifest)
        return Response(manifest)


@INCLUDE_EXCLUDE_FIELDS_SCHEMA
class ProductVariantViewSetSet(ProductDataViewSet):
    """View for api/v1/product_variants"""

    queryset = ProductVariant.objects.order_by(ProductDataViewSet.ordering_field).using("read_only")
    serializer_class = ProductVariantSerializer

    def list(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        req = self.request
        ofuri = req.query_params.get("ofuri")
        if not ofuri:
            return super().list(request)
        return super().retrieve(request)

    def get_object(self):
        req = self.request
        pv_ofuri = req.query_params.get("ofuri")
        pv_name = req.query_params.get("name")
        try:
            if pv_name:
                pv = ProductVariant.objects.db_manager("read_only").get(name=pv_name)
            elif pv_ofuri:
                pv = ProductVariant.objects.db_manager("read_only").get(ofuri=pv_ofuri)
            else:
                pk = req.path.split("/")[-1]  # there must be better ways ...
                pv = ProductVariant.objects.db_manager("read_only").get(uuid=pk)
            return pv
        except ProductVariant.DoesNotExist:
            raise Http404


@INCLUDE_EXCLUDE_FIELDS_SCHEMA
class ChannelViewSet(ReadOnlyModelViewSet):
    """View for api/v1/channels"""

    queryset = Channel.objects.order_by("name").using("read_only")
    serializer_class = ChannelSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ChannelFilter
    lookup_url_kwarg = "uuid"


@INCLUDE_EXCLUDE_FIELDS_SCHEMA
class ComponentViewSet(ReadOnlyModelViewSet):  # TODO: TagViewMixin disabled until auth is added
    """View for api/v1/components"""

    queryset = (
        Component.objects.order_by("name", "type", "arch", "version", "release")
        .using("read_only")
        .select_related("software_build")
    )
    serializer_class: Union[
        Type[ComponentSerializer], Type[ComponentListSerializer]
    ] = ComponentSerializer
    search_fields = ["name", "description", "release", "version", "meta_attr"]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ComponentFilter
    lookup_url_kwarg = "uuid"

    def get_queryset(self) -> QuerySet[Component]:
        # 'latest' filter only relevant in terms of a specific offering/product
        ofuri = self.request.query_params.get("ofuri")
        if not ofuri:
            return self.queryset

        model, _ = get_model_ofuri_type(ofuri)
        if isinstance(model, Product):
            return self.queryset.filter(products__ofuri=ofuri)
        elif isinstance(model, ProductVersion):
            return self.queryset.filter(productversions__ofuri=ofuri)
        elif isinstance(model, ProductStream):
            # only ProductStream defines get_latest_components()
            # TODO: Should this be a ProductModel method? For e.g. Products,
            #  we could return get_latest_components() for each child stream
            return model.get_latest_components()
        elif isinstance(model, ProductVariant):
            return self.queryset.filter(productvariants__ofuri=ofuri)
        else:
            # No matching model instance found, or invalid ofuri
            raise Http404

    @extend_schema(
        parameters=[
            OpenApiParameter("ofuri", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("view", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("purl", OpenApiTypes.STR, OpenApiParameter.QUERY),
        ]
    )
    def list(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        # purl are stored with each segment url encoded as per the specification. The purl query
        # param here is url decoded, to ensure special characters such as '@' and '?'
        # are not interpreted as part of the request.
        view = request.query_params.get("view")
        purl = request.query_params.get("purl")
        component_name = self.request.query_params.get("name")
        component_re_name = self.request.query_params.get("re_name")
        if not purl:
            # TODO: ?name={}&view=latest this may turn out to be temporary
            if (component_re_name or component_name) and view == "latest":
                ps_cond = {}
                strict_search = True
                if component_re_name:
                    strict_search = False
                    component_name = component_re_name
                    ps_cond["name__iregex"] = component_name
                else:
                    ps_cond["name"] = component_name  # type: ignore
                latest_components = []
                product_stream_ofuris = list(
                    set(
                        self.get_queryset()
                        .filter(**ps_cond)
                        .values_list("productstreams__ofuri", flat=True)
                        .using("read_only")
                    )
                )
                for ps_ofuri in product_stream_ofuris:
                    ps = ProductStream.objects.filter(ofuri=ps_ofuri, active=True).first()
                    if ps:
                        ps_components = ps.get_latest_components(
                            component_name, strict_search=strict_search
                        )
                        for ps_component in ps_components:
                            component = {
                                "product_version": ps.productversions.name,
                                "product_version_ofuri": ps.productversions.ofuri,
                                "product_stream": ps.name,
                                "product_stream_ofuri": ps.ofuri,
                                "product_active": ps.active,
                                "purl": ps_component.purl,
                                "type": ps_component.type,
                                "namespace": ps_component.namespace,
                                "name": ps_component.name,
                                "release": ps_component.release,
                                "version": ps_component.version,
                                "nvr": ps_component.nvr,
                                "build_id": None,
                                "build_type": None,
                                "build_source_url": None,
                                "related_url": None,
                                "upstream_purl": None,
                            }
                            if ps_component.software_build:
                                component["build_id"] = ps_component.software_build.build_id
                                component["build_type"] = ps_component.software_build.build_type
                                component["build_source_url"] = ps_component.software_build.source
                            if ps_component.upstreams.all():
                                component["related_url"] = ps_component.upstreams.all().first().related_url  # type: ignore # noqa
                                component["upstream_purl"] = ps_component.upstreams.all().first().purl  # type: ignore # noqa
                            latest_components.append(component)
                return Response({"results": latest_components})
            if view == "product":
                component_name = self.request.query_params.get("name")
                product_streams_arr = []
                for c in (
                    self.get_queryset()
                    .filter(name=component_name)
                    .prefetch_related("productstreams")
                ):
                    annotated_ps_qs = (
                        c.productstreams.get_queryset()
                        .annotate(component_purl=Value(c.purl))
                        .using("read_only")
                    )
                    product_streams_arr.append(annotated_ps_qs)

                ps_qs = ProductStream.objects.none()
                productstreams = ps_qs.union(*product_streams_arr).using("read_only")
                serializer = ComponentProductStreamSummarySerializer(
                    productstreams, many=True, read_only=True
                )
                return Response({"count": productstreams.count(), "results": serializer.data})
            if view == "summary":
                self.serializer_class = ComponentListSerializer
            return super().list(request)
        return super().retrieve(request)

    def get_object(self):
        req = self.request
        purl = req.query_params.get("purl")
        try:
            if purl:
                # We re-encode the purl here to ensure each segment of the purl is url encoded,
                # as it's stored in the DB.
                purl = f"{PackageURL.from_string(purl)}"
                component = Component.objects.db_manager("read_only").get(purl=purl)
            else:
                pk = req.path.split("/")[-1]  # there must be better ways ...
                component = Component.objects.db_manager("read_only").get(uuid=pk)
            return component
        except Component.DoesNotExist:
            raise Http404

    @action(methods=["get"], detail=True)
    def manifest(self, request: Request, uuid: str = "") -> Response:
        obj = self.queryset.filter(uuid=uuid).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        manifest = json.loads(obj.manifest)
        return Response(manifest)

    @action(methods=["put"], detail=True)
    def olcs_test(self, request: Request, uuid: Union[str, None] = None) -> Response:
        """Allow OpenLCS to upload copyright text / license scan results for a component"""
        # In the future these could be separate endpoints
        # For testing we'll just keep it under one endpoint
        if utils.running_prod():
            # This is only temporary for OpenLCS testing
            # Do not enable in production until we add OIDC authentication
            return Response(status=status.HTTP_403_FORBIDDEN)
        component = self.queryset.filter(uuid=uuid).using("default").first()
        if not component:
            return Response(status=status.HTTP_404_NOT_FOUND)

        copyright_text = request.data.get("copyright_text")
        license_concluded = request.data.get("license_concluded")
        license_declared = request.data.get("license_declared")
        openlcs_scan_url = request.data.get("openlcs_scan_url")
        openlcs_scan_version = request.data.get("openlcs_scan_version")
        if (
            not copyright_text
            and not license_concluded
            and not license_declared
            and not openlcs_scan_url
            and not openlcs_scan_version
        ):
            # At least one of above is required, else Bad Request
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # if it's None, it wasn't included in the request
        # But it might be "" if the user wants to empty out the value
        if copyright_text is not None:
            component.copyright_text = copyright_text
        if license_concluded is not None:
            component.license_concluded_raw = license_concluded
        if license_declared is not None:
            if component.license_declared_raw:
                # The field already has an existing value, don't allow overwrites
                return Response(status=status.HTTP_400_BAD_REQUEST)
            component.license_declared_raw = license_declared
        if openlcs_scan_url is not None:
            component.openlcs_scan_url = openlcs_scan_url
        if openlcs_scan_version is not None:
            component.openlcs_scan_version = openlcs_scan_version
        component.save()
        response = Response(status=status.HTTP_302_FOUND)
        response["Location"] = f"/api/{CORGI_API_VERSION}/components/{component.uuid}"
        return response

    @action(methods=["get"], detail=True)
    def provides(self, request: Request, uuid: Union[str, None] = None) -> Response:
        obj = self.queryset.filter(uuid=uuid).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        dicts = get_component_taxonomy(
            obj,
            ComponentNode.PROVIDES_NODE_TYPES,
        )
        return Response(dicts)

    @action(methods=["get"], detail=True)
    def taxonomy(self, request: Request, uuid: Union[str, None] = None) -> Response:
        obj = self.queryset.filter(uuid=uuid).first()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        dicts = get_component_taxonomy(obj, tuple(ComponentNode.ComponentNodeType.values))
        return Response(dicts)


class AppStreamLifeCycleViewSet(ReadOnlyModelViewSet):
    """View for api/v1/lifecycles"""

    queryset = AppStreamLifeCycle.objects.order_by(
        "name", "type", "product", "initial_product_version", "stream"
    ).using("read_only")
    serializer_class = AppStreamLifeCycleSerializer
