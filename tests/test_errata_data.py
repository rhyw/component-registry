from unittest.mock import patch

import pytest
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from corgi.collectors.models import (
    CollectorErrataProduct,
    CollectorErrataProductVariant,
    CollectorErrataProductVersion,
    CollectorRPMRepository,
)
from corgi.core.models import (
    Channel,
    ProductComponentRelation,
    ProductNode,
    ProductVariant,
)
from corgi.tasks.errata_tool import slow_load_errata, update_variant_repos

from .factories import ProductStreamFactory, ProductVariantFactory

pytestmark = [pytest.mark.unit, pytest.mark.django_db]


def test_update_variant_repos():
    sap_variant = "SAP-8.4.0.Z.EUS"
    sap_repos = [
        "rhel-8-for-ppc64le-sap-netweaver-e4s-debug-rpms__8_DOT_4",
        "rhel-8-for-ppc64le-sap-netweaver-e4s-rpms__8_DOT_4",
    ]
    ha_variants = (
        "HighAvailability-8.2.0.GA",
        "HighAvailability-8.3.0.GA",
    )

    ha_repos = [
        "rhel-8-for-aarch64-highavailability-debug-rpms__8",
        "rhel-8-for-aarch64-highavailability-rpms__8",
    ]
    ps = ProductStreamFactory.create(name="rhel", version="8.2.0")
    product_node = ProductNode.objects.create(parent=None, obj=ps.products)
    pv_node = ProductNode.objects.create(parent=product_node, obj=ps.productversions)
    ps_node = ProductNode.objects.create(parent=pv_node, obj=ps)

    et_id = 0
    setup_models_for_variant_repos(sap_repos, ps_node, sap_variant, et_id)
    for variant in ha_variants:
        et_id += 1
        setup_models_for_variant_repos(ha_repos, ps_node, variant, et_id)

    update_variant_repos()

    pv = ProductVariant.objects.get(name="SAP-8.4.0.Z.EUS")
    assert pv.pnodes.count() == 1
    pv_node = pv.pnodes.first()
    assert (
        sorted(pv.channels.values_list("name", flat=True))
        == [channel_node.obj.name for channel_node in pv_node.get_descendants()]
        == sap_repos
    )
    # Check that every channel for this Product Variant point to only a single Channel Node since
    # this Variant does not share its repos with any of the HA Variants.
    assert all(channel_node.obj.pnodes.count() == 1 for channel_node in pv_node.get_descendants())

    # HA Variants share the same set of repos, so check that one Channel entity exists that links
    # to two separate pnodes whose immediate parents are the Variants themselves.
    for repo in ha_repos:
        channel = Channel.objects.get(type=Channel.Type.CDN_REPO, name=repo)
        assert channel.pnodes.count() == 2
        assert (
            channel.pnodes.order_by("id")
            .first()
            .get_ancestors()
            .filter(content_type=ContentType.objects.get_for_model(ProductVariant))
            .first()
            .obj.name
            == "HighAvailability-8.2.0.GA"
        )
        assert (
            channel.pnodes.order_by("id")
            .last()
            .get_ancestors()
            .filter(content_type=ContentType.objects.get_for_model(ProductVariant))
            .first()
            .obj.name
            == "HighAvailability-8.3.0.GA"
        )


def setup_models_for_variant_repos(repos, ps_node, variant, et_id):
    et_product = CollectorErrataProduct.objects.create(
        et_id=et_id, name=f"name-{et_id}", short_name=str(et_id)
    )
    et_product_version = CollectorErrataProductVersion.objects.create(
        et_id=et_id, name=f"name-{et_id}", product=et_product
    )
    CollectorErrataProductVariant.objects.create(
        name=variant, repos=repos, et_id=et_id, product_version=et_product_version
    )
    for repo in repos:
        CollectorRPMRepository.objects.get_or_create(name=repo)

    pv = ProductVariantFactory.create(name=variant)
    ProductNode.objects.create(object_id=pv.pk, obj=pv, parent=ps_node)


# id, no_of_obj
errata_details = [
    (
        "77149",
        """    {
          "RHEL-8.4.0.Z.MAIN+EUS": {
            "name": "RHEL-8.4.0.Z.MAIN+EUS",
            "description": "Red Hat Enterprise Linux 8",
            "builds": [
              {
                "ca-certificates-2021.2.50-80.0.el8_4": {
                  "nvr": "ca-certificates-2021.2.50-80.0.el8_4",
                  "nevr": "ca-certificates-0:2021.2.50-80.0.el8_4",
                  "id": 1636922,
                  "is_module": false,
                  "variant_arch": {
                    "BaseOS-8.4.0.Z.MAIN.EUS": {
                      "SRPMS": [
                        "ca-certificates-2021.2.50-80.0.el8_4.src.rpm"
                      ],
                      "noarch": [
                        "ca-certificates-2021.2.50-80.0.el8_4.noarch.rpm"
                      ]
                    }
                  },
                  "added_by": null
                }
              }
            ]
          }
    }""",
        1,
    ),
    (
        "77150",
        """{
            "RHEL-7-dotNET-3.1": {
              "name": "RHEL-7-dotNET-3.1",
              "description": ".NET Core on Red Hat Enterprise Linux",
              "builds": [
                {
                  "rh-dotnet31-runtime-container-3.1-18": {
                    "nvr": "rh-dotnet31-runtime-container-3.1-18",
                    "nevr": "rh-dotnet31-runtime-container-0:3.1-18",
                    "id": 1628352,
                    "is_module": false,
                    "variant_arch": {
                      "7Server-dotNET-3.1": {
                        "multi": [
                          "docker-image-sha256:20952dbe8bf1159496be299778aaf44a5e50880f10c7689a38c3113c64b70d11.x86_64.tar.gz"
                        ]
                      }
                    },
                    "added_by": null
                  }
                },
                {
                  "rh-dotnet31-container-3.1-18": {
                    "nvr": "rh-dotnet31-container-3.1-18",
                    "nevr": "rh-dotnet31-container-0:3.1-18",
                    "id": 1628358,
                    "is_module": false,
                    "variant_arch": {
                      "7Server-dotNET-3.1": {
                        "multi": [
                          "docker-image-sha256:5f398886270c47b7d8c25f06093202d50cd49866e6f8dee48b6535e9ca144c6f.x86_64.tar.gz"
                        ]
                      }
                    },
                    "added_by": null
                  }
                },
                {
                  "rh-dotnet31-jenkins-agent-container-3.1-27": {
                    "nvr": "rh-dotnet31-jenkins-agent-container-3.1-27",
                    "nevr": "rh-dotnet31-jenkins-agent-container-0:3.1-27",
                    "id": 1628450,
                    "is_module": false,
                    "variant_arch": {
                      "7Server-dotNET-3.1": {
                        "multi": [
                          "docker-image-sha256:883da35d429fae52f0c1b2e7e9e36368d71577baa2334d5e9efc6d1f12d1c898.x86_64.tar.gz"
                        ]
                      }
                    },
                    "added_by": null
                  }
                }
              ]
            }
        }""",
        3,
    ),
]


@patch("config.celery.app.send_task")
@pytest.mark.parametrize("erratum_id, build_list, no_of_objs", errata_details)
def test_save_product_component_for_errata(
    mock_send, erratum_id, build_list, no_of_objs, requests_mock
):
    build_list_url = f"{settings.ERRATA_TOOL_URL}/api/v1/erratum/{erratum_id}/builds_list.json"
    requests_mock.get(build_list_url, text=build_list)
    slow_load_errata(erratum_id)
    pcr = ProductComponentRelation.objects.filter(external_system_id=erratum_id)
    assert len(pcr) == no_of_objs
    assert mock_send.call_count == no_of_objs
