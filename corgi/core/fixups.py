# This is a temporary mapping of Product Streams, for which we can generate and publish SBOMs.
# This data should be moved to an appropriate object in product definitions as soon as possible.
supported_stream_cpes = {
    "3amp-2": ["cpe:/a:redhat:3scale_amp:2.12::el7", "cpe:/a:redhat:3scale_amp:2.12::el8"],
    "amq-ic-1": [
        "cpe:/a:redhat:amq_interconnect:1::el7",
        "cpe:/a:redhat:amq_interconnect:1::el8",
        "cpe:/a:redhat:amq_interconnect:1::el7",
        "cpe:/a:redhat:amq_interconnect:1::el7",
    ],
    "ansible_automation_platform-1.2": ["cpe:/a:redhat:ansible_automation_platform:3.8::el7"],
    "ansible_automation_platform-2.1": [
        "cpe:/a:redhat:ansible_automation_platform_developer:2.1::el8",
        "cpe:/a:redhat:ansible_automation_platform:2.1::el8",
        "cpe:/a:redhat:ansible_automation_platform_azure_billing:2.1::el8",
    ],
    "ansible_automation_platform-2.2": [
        "cpe:/a:redhat:ansible_automation_platform_inside:2.2::el8",
        "cpe:/a:redhat:ansible_automation_platform_developer:2.2::el8",
        "cpe:/a:redhat:ansible_automation_platform_inside:2.2::el9",
        "cpe:/a:redhat:ansible_inside:0.9::el9",
        "cpe:/a:redhat:ansible_inside:0.9::el8",
        "cpe:/a:redhat:ansible_automation_platform:2.2::el8",
        "cpe:/a:redhat:ansible_automation_platform_developer:2.2::el9",
        "cpe:/a:redhat:ansible_automation_platform:2.2::el9",
        "cpe:/a:redhat:ansible_automation_platform_azure_billing:2.2::el8",
    ],
    "ansible_automation_platform-2.3": [
        "cpe:/a:redhat:ansible_inside:1.0::el9",
        "cpe:/a:redhat:ansible_automation_platform_inside:2.3::el8",
        "cpe:/a:redhat:ansible_inside:1.0::el8",
        "cpe:/a:redhat:ansible_developer:1.0::el8",
        "cpe:/a:redhat:ansible_automation_platform_cloud_billing:2.3::el8",
        "cpe:/a:redhat:ansible_automation_platform_developer:2.3::el8",
        "cpe:/a:redhat:ansible_automation_platform:2.3::el9",
        "cpe:/a:redhat:ansible_automation_platform_developer:2.3::el9",
        "cpe:/a:redhat:ansible_automation_platform_developer:2.3::el8",
        "cpe:/a:redhat:ansible_developer:1.0::el9",
        "cpe:/a:redhat:ansible_automation_platform_developer:2.3::el9",
        "cpe:/a:redhat:ansible_automation_platform:2.3::el8",
        "cpe:/a:redhat:ansible_automation_platform_inside:2.3::el9",
    ],
    "ceph-3": [
        "cpe:/a:redhat:ceph_storage:3::el7",
        "cpe:/a:redhat:ceph_storage:3::el7",
        "cpe:/a:redhat:ceph_storage:3::el7",
        "cpe:/a:redhat:ceph_storage:3::el7",
        "cpe:/a:redhat:ceph_storage:3::el7",
        "cpe:/a:redhat:ceph_storage:3::el7",
    ],
    "ceph-4": [
        "cpe:/a:redhat:ceph_storage:4::el7",
        "cpe:/a:redhat:ceph_storage:4::el8",
        "cpe:/a:redhat:ceph_storage:4::el7",
        "cpe:/a:redhat:ceph_storage:4::el8",
        "cpe:/a:redhat:ceph_storage:4::el7",
        "cpe:/a:redhat:ceph_storage:4::el8",
    ],
    "ceph-5": [
        "cpe:/a:redhat:ceph_storage:5.1::el8",
        "cpe:/a:redhat:ceph_storage:5.1::el8",
        "cpe:/a:redhat:ceph_storage:5.1::el8",
    ],
    "certificate_system_10.2.z": [
        "cpe:/a:redhat:certificate_system_eus:10.2::el8",
        "cpe:/a:redhat:certificate_system:10.2::el8",
    ],
    "certificate_system_10.4.z": ["cpe:/a:redhat:certificate_system:10.4::el8"],
    "cert-manager-1": ["cpe:/a:redhat:cert_manager:1.10::el9"],
    "cfme-5.11": ["cpe:/a:redhat:cloudforms_managementengine:5.11::el8"],
    "cma-2": ["cpe:/a:redhat:openshift_custom_metrics_autoscaler:2.6::el8"],
    "cnv-4.10": [
        "cpe:/a:redhat:container_native_virtualization:4.10::el8",
        "cpe:/a:redhat:container_native_virtualization:4.10::el7",
    ],
    "cnv-4.11": [
        "cpe:/a:redhat:container_native_virtualization:4.11::el7",
        "cpe:/a:redhat:container_native_virtualization:4.11::el8",
    ],
    "cnv-4.12": [
        "cpe:/a:redhat:container_native_virtualization:4.12::el7",
        "cpe:/a:redhat:container_native_virtualization:4.12::el8",
    ],
    "convert2rhel-7": ["cpe:/a:redhat:convert2rhel::el7"],
    "convert2rhel-8": ["cpe:/a:redhat:convert2rhel::el8"],
    "cryostat-2": ["cpe:/a:redhat:cryostat:2::el8"],
    "devtools-compilers-2022-4.z": ["cpe:/a:redhat:devtools:2022"],
    "directory_server_11.5": ["cpe:/a:redhat:directory_server:11.5::el8"],
    "directory_server_11.6": ["cpe:/a:redhat:directory_server:11.6::el8"],
    "directory_server_12.0": [
        "cpe:/a:redhat:directory_server_eus:12::el9",
        "cpe:/a:redhat:directory_server:12::el9",
    ],
    "directory_server_12.1": ["cpe:/a:redhat:directory_server:12.1::el9"],
    "dotnet-6.0": [
        "cpe:/a:redhat:rhel_dotnet:6.0::el7",
        "cpe:/a:redhat:rhel_dotnet:6.0::el7",
        "cpe:/a:redhat:rhel_dotnet:6.0::el7",
    ],
    "dts-11.1.z": ["cpe:/a:redhat:rhel_software_collections:3::el7"],
    "dts-12.0.z": ["cpe:/a:redhat:rhel_software_collections:3::el7"],
    "dts-12.1": ["cpe:/a:redhat:rhel_software_collections:3::el7"],
    "fdp-el7-ovs": ["cpe:/o:redhat:enterprise_linux:7::fastdatapath"],
    "fdp-el8-ovs": ["cpe:/o:redhat:enterprise_linux:8::fastdatapath"],
    "fdp-el9": ["cpe:/o:redhat:enterprise_linux:9::fastdatapath"],
    "gitops-1.6.z": ["cpe:/a:redhat:openshift_gitops:1.6::el8"],
    "gitops-1.7": ["cpe:/a:redhat:openshift_gitops:1.7::el8"],
    "gitops-1.8": ["cpe:/a:redhat:openshift_gitops:1.8::el8"],
    "gitops-1.9": ["cpe:/a:redhat:openshift_gitops:1.9::el9"],
    "kmm-1": [
        "cpe:/a:redhat:kernel_module_management:1.0::el8",
        "cpe:/a:redhat:kernel_module_management:1.0::el9",
    ],
    "mta-6.0": ["cpe:/a:redhat:migration_toolkit_applications:6.0::el8"],
    "mta-6.1.z": ["cpe:/a:redhat:migration_toolkit_applications:6.1::el8"],
    "mtc-1.7": ["cpe:/a:redhat:rhmt:1.7::el7", "cpe:/a:redhat:rhmt:1.7::el8"],
    "mtr-1.0": ["cpe:/a:redhat:migration_toolkit_runtimes:1.0::el8"],
    "mtv-2.2": ["cpe:/a:redhat:migration_toolkit_virtualization:2.2::el8"],
    "mtv-2.3": ["cpe:/a:redhat:migration_toolkit_virtualization:2.3::el8"],
    "nhc-0.3.z": [
        "cpe:/a:redhat:workload_availability_node_healthcheck:0.3::el8",
        "cpe:/a:redhat:workload_availability_node_healthcheck:0.3::el8",
    ],
    "nmo-4.11": ["cpe:/a:redhat:workload_availability_node_maintenance:4.11::el8"],
    "noo-1": ["cpe:/a:redhat:network_observ_optr:1.0.0::el8"],
    "oadp-1.0": ["cpe:/a:redhat:openshift_api_data_protection:1.0::el8"],
    "oadp-1.1": ["cpe:/a:redhat:openshift_api_data_protection:1.1::el8"],
    "ocp-tools-4.11": ["cpe:/a:redhat:ocp_tools:4.11::el8"],
    "ocp-tools-4.12": ["cpe:/a:redhat:ocp_tools:4.12::el8"],
    "ocp-tools-4.13": ["cpe:/a:redhat:ocp_tools:4.13::el8"],
    "rhes-3.5": [
        "cpe:/a:redhat:storage:3.5:nfs:el7",
        "cpe:/a:redhat:storage:3.5:na:el7",
        "cpe:/a:redhat:storage:3.5:samba:el7",
        "cpe:/a:redhat:storage:3.5:server:el7",
        "cpe:/a:redhat:storage:3.5:wa:el7",
        "cpe:/a:redhat:storage:3.5:nfs:el8",
        "cpe:/a:redhat:storage:3.5:na:el8",
        "cpe:/a:redhat:storage:3.5:samba:el8",
        "cpe:/a:redhat:storage:3.5:server:el8",
        "cpe:/a:redhat:storage:3.5:wa:el8",
    ],
    "omr-1": ["cpe:/a:redhat:mirror_registry:1.1.0::el8"],
    "openshift-4.10.z": ["cpe:/a:redhat:openshift:4.10::el8", "cpe:/a:redhat:openshift:4.10::el7"],
    "openshift-4.11.z": ["cpe:/a:redhat:openshift:4.11::el7", "cpe:/a:redhat:openshift:4.11::el8"],
    "openshift-4.12.z": [
        "cpe:/a:redhat:openshift:4.12::el8",
        "cpe:/a:redhat:openshift:4.12::el9",
        "cpe:/a:redhat:openshift_ironic:4.12::el9",
    ],
    "openshift-4.13": [
        "cpe:/a:redhat:openshift:4.13::el8",
        "cpe:/a:redhat:openshift:4.13::el9",
        "cpe:/a:redhat:openshift_ironic:4.13::el9",
    ],
    "openshift-enterprise-3.11.z": ["cpe:/a:redhat:openshift:3.11::el7"],
    "openshift-logging-5.4": ["cpe:/a:redhat:logging:5.4::el8"],
    "openshift-logging-5.5": ["cpe:/a:redhat:logging:5.5::el8"],
    "openshift-logging-5.6": ["cpe:/a:redhat:logging:5.6::el8"],
    "openshift-logging-5.7": ["cpe:/a:redhat:logging:5.7::el8"],
    "openshift-container-storage-4.8.z": ["cpe:/a:redhat:openshift_container_storage:4.8::el8"],
    "openshift-data-foundation-4.10.z": ["cpe:/a:redhat:openshift_data_foundation:4.10::el8"],
    "openshift-data-foundation-4.11.z": ["cpe:/a:redhat:openshift_data_foundation:4.11::el8"],
    "openshift-data-foundation-4.12.z": ["cpe:/a:redhat:openshift_data_foundation:4.12::el8"],
    "openshift-data-foundation-4.9.z": ["cpe:/a:redhat:openshift_data_foundation:4.9::el8"],
    "openstack-13-els": ["cpe:/a:redhat:openstack:13::el7"],
    "openstack-13-optools": ["cpe:/a:redhat:openstack-optools:13::el7"],
    "openstack-16.1": [
        "cpe:/a:redhat:openstack:16.1::el8",
        "cpe:/a:redhat:openstack:16.1::el8",
        "cpe:/a:redhat:openstack:16.1::el8",
        "cpe:/a:redhat:openstack:16.1::el8",
        "cpe:/a:redhat:openstack:16.1::el8",
    ],
    "openstack-16.2": [
        "cpe:/a:redhat:openstack:16.2::el8",
        "cpe:/a:redhat:openstack:16.2::el8",
        "cpe:/a:redhat:openstack:16.2::el8",
        "cpe:/a:redhat:openstack:16.2::el8",
    ],
    "openstack-17.0": [
        "cpe:/a:redhat:openstack:17.0::el9",
        "cpe:/a:redhat:openstack:17.0::el9",
        "cpe:/a:redhat:openstack:17.0::el9",
        "cpe:/a:redhat:openstack:17.0::el9",
    ],
    "ossm-2.1": ["cpe:/a:redhat:service_mesh:2.1::el8", "cpe:/a:redhat:service_mesh:2.1::el7"],
    "ossm-2.2": ["cpe:/a:redhat:service_mesh:2.2::el8"],
    "ossm-2.3": ["cpe:/a:redhat:service_mesh:2.3::el8"],
    "osso-1": ["cpe:/a:redhat:openshift_secondary_scheduler:1.1::el8"],
    "pipelines-1.10": ["cpe:/a:redhat:openshift_pipelines:1.10::el8"],
    "pipelines-1.6.2": ["cpe:/a:redhat:openshift_pipelines:1.6::el8"],
    "pipelines-1.7": ["cpe:/a:redhat:openshift_pipelines:1.7::el8"],
    "pipelines-1.7.1": ["cpe:/a:redhat:openshift_pipelines:1.7::el8"],
    "pipelines-1.8": ["cpe:/a:redhat:openshift_pipelines:1.8::el8"],
    "pipelines-1.8.1": ["cpe:/a:redhat:openshift_pipelines:1.8::el8"],
    "pipelines-1.9": ["cpe:/a:redhat:openshift_pipelines:1.9::el8"],
    "quay-3.6": ["cpe:/a:redhat:quay:3::el8"],
    "quay-3.7": ["cpe:/a:redhat:quay:3::el8"],
    "quay-3.8": ["cpe:/a:redhat:quay:3::el8"],
    "rhacm-2.5.z": ["cpe:/a:redhat:acm:2.5::el8"],
    "rhacm-2.6.z": ["cpe:/a:redhat:acm:2.6::el8"],
    "rhacm-2.7": ["cpe:/a:redhat:acm:2.7::el8"],
    "rhacs-3.72": ["cpe:/a:redhat:advanced_cluster_security:3.72::el8"],
    "rhacs-3.73": ["cpe:/a:redhat:advanced_cluster_security:3.73::el8"],
    "rhacs-3.74": ["cpe:/a:redhat:advanced_cluster_security:3.74::el8"],
    "rhacs-4.0": ["cpe:/a:redhat:advanced_cluster_security:4.0::el8"],
    "rhapi-1": [
        "cpe:/a:redhat:application_interconnect:1::el8",
        "cpe:/a:redhat:application_interconnect:1::el9",
    ],
    "rhel-7.9.z": [
        "cpe:/o:redhat:enterprise_linux:7::server",
        "cpe:/o:redhat:enterprise_linux:7::computenode",
        "cpe:/a:redhat:rhel_extras_other:7",
        "cpe:/a:redhat:rhel_extras_rt:7",
        "cpe:/a:redhat:rhel_extras:7",
        "cpe:/a:redhat:rhel_extras_other:7",
        "cpe:/o:redhat:enterprise_linux:7::server",
        "cpe:/a:redhat:rhel_extras_sap_hana:7",
        "cpe:/o:redhat:enterprise_linux:7::server",
        "cpe:/a:redhat:rhel_extras_other:7",
        "cpe:/o:redhat:enterprise_linux:7::workstation",
        "cpe:/a:redhat:rhel_extras:7",
        "cpe:/o:redhat:enterprise_linux:7::server",
        "cpe:/a:redhat:rhel_extras:7",
        "cpe:/a:redhat:rhel_extras_rt:7",
        "cpe:/o:redhat:enterprise_linux:7::computenode",
        "cpe:/o:redhat:enterprise_linux:7::workstation",
        "cpe:/a:redhat:rhel_extras_sap:7",
        "cpe:/a:redhat:enterprise_linux:7",
        "cpe:/o:redhat:enterprise_linux:7::client",
        "cpe:/o:redhat:enterprise_linux:7::client",
        "cpe:/a:redhat:rhel_extras:7",
    ],
    "rhel-8.8.0": [
        "cpe:/a:redhat:enterprise_linux:8::appstream",
        "cpe:/a:redhat:enterprise_linux:8::crb",
        "cpe:/a:redhat:enterprise_linux:8::highavailability",
        "cpe:/a:redhat:enterprise_linux:8::nfv",
        "cpe:/a:redhat:enterprise_linux:8::realtime",
        "cpe:/a:redhat:enterprise_linux:8::resilientstorage",
        "cpe:/a:redhat:enterprise_linux:8::sap",
        "cpe:/a:redhat:enterprise_linux:8::sap_hana",
        "cpe:/a:redhat:enterprise_linux:8::supplementary",
        "cpe:/o:redhat:enterprise_linux:8::baseos",
        "cpe:/o:redhat:enterprise_linux:8::fastdatapath",
        "cpe:/o:redhat:enterprise_linux:8::hypervisor",
    ],
    "rhel-9.2.0": [
        "cpe:/a:redhat:enterprise_linux:9::appstream",
        "cpe:/a:redhat:enterprise_linux:9::crb",
        "cpe:/a:redhat:enterprise_linux:9::highavailability",
        "cpe:/a:redhat:enterprise_linux:9::nfv",
        "cpe:/a:redhat:enterprise_linux:9::realtime",
        "cpe:/a:redhat:enterprise_linux:9::resilientstorage",
        "cpe:/a:redhat:enterprise_linux:9::sap",
        "cpe:/a:redhat:enterprise_linux:9::sap_hana",
        "cpe:/a:redhat:enterprise_linux:9::supplementary",
        "cpe:/o:redhat:enterprise_linux:9::baseos",
        "cpe:/o:redhat:enterprise_linux:9::fastdatapath",
        "cpe:/o:redhat:enterprise_linux:9::hypervisor",
    ],
    "rhel-av-8.4.0.z": ["cpe:/a:redhat:advanced_virtualization:8.4::el8"],
    "rhev-m-4.4.z": [
        "cpe:/o:redhat:enterprise_linux:8::hypervisor",
        "cpe:/o:redhat:enterprise_linux:8::hypervisor",
        "cpe:/o:redhat:enterprise_linux:8::hypervisor",
        "cpe:/o:redhat:enterprise_linux:8::hypervisor",
        "cpe:/a:redhat:rhev_manager:4.4:el8",
    ],
    "rhn_satellite_6.10": [
        "cpe:/a:redhat:satellite_capsule:6.10::el7",
        "cpe:/a:redhat:satellite:6.10::el7",
    ],
    "rhn_satellite_6.11": [
        "cpe:/a:redhat:satellite:6.11::el7",
        "cpe:/a:redhat:rhel_satellite_client:6::el7",
        "cpe:/a:redhat:satellite_utils:6.11::el7",
        "cpe:/a:redhat:rhel_satellite_client:6::el8",
        "cpe:/a:redhat:rhel_satellite_client:6::el7",
        "cpe:/a:redhat:rhel_satellite_client:6::el7",
        "cpe:/a:redhat:satellite_maintenance:6.11::el7",
        "cpe:/a:redhat:satellite_utils:6.11::el8",
        "cpe:/a:redhat:satellite_capsule:6.11::el7",
        "cpe:/a:redhat:satellite:6.11::el8",
        "cpe:/a:redhat:rhel_satellite_client:6::el9",
        "cpe:/a:redhat:satellite_maintenance:6.11::el8",
        "cpe:/a:redhat:satellite_capsule:6.11::el8",
        "cpe:/a:redhat:rhel_satellite_client:6::el6",
        "cpe:/a:redhat:rhel_satellite_client:6::el7",
    ],
    "rhn_satellite_6.12": [
        "cpe:/a:redhat:satellite_utils:6.12::el8",
        "cpe:/a:redhat:satellite_maintenance:6.12::el8",
        "cpe:/a:redhat:satellite:6.12::el8",
        "cpe:/a:redhat:satellite_capsule:6.12::el8",
    ],
    "rhn_satellite_6.13": [
        "cpe:/a:redhat:satellite:6.13::el8",
        "cpe:/a:redhat:satellite_capsule:6.13::el8",
        "cpe:/a:redhat:satellite_maintenance:6.13::el8",
        "cpe:/a:redhat:satellite_utils:6.13::el8",
    ],
    "rhods-1.20": ["cpe:/a:redhat:openshift_data_science:1.20::el8"],
    "rhods-1.21": ["cpe:/a:redhat:openshift_data_science:1.21::el8"],
    "rhods-1.23": ["cpe:/a:redhat:openshift_data_science:1.23::el8"],
    "rhods-1.24": ["cpe:/a:redhat:openshift_data_science:1.24::el8"],
    "rhosc-1": ["cpe:/a:redhat:openshift_sandboxed_containers:1.3.0::el8"],
    "rhos_devspaces-3": ["cpe:/a:redhat:openshift_devspaces:3::el8"],
    "rhosdt-2": ["cpe:/a:redhat:openshift_distributed_tracing:2.3::el8"],
    "rhscl-3.8.z": [
        "cpe:/a:redhat:rhel_software_collections:3::el6",
        "cpe:/a:redhat:rhel_software_collections:3::el7",
    ],
    "rhui-4": ["cpe:/a:redhat:rhui:4::el8"],
    "rodoo-1": ["cpe:/a:redhat:run_once_duration_override_operator:1.0::el8"],
    "rosa-cli-1": ["cpe:/a:redhat:openshift_service_on_aws:1::el8"],
    "snr-0.4.z": ["cpe:/a:redhat:workload_availability_self_node_remediation:0.4::el8"],
    "srvcom-1": ["cpe:/a:redhat:serverless:1.0::el8", "cpe:/a:redhat:serverless:1.25::el8"],
    "stf-1.4": ["cpe:/a:redhat:service_telemetry_framework:1.4::el8"],
    "stf-1.5": ["cpe:/a:redhat:service_telemetry_framework:1.5::el8"],
    "wto-1.5": ["cpe:/a:redhat:webterminal:1.5::el8"],
    "rhcertification-6": ["cpe:/a:redhat:certifications:1::el6"],
    "rhcertification-7": ["cpe:/a:redhat:certifications:1::el7"],
    "rhcertification-8": ["cpe:/a:redhat:certifications:1::el8"],
    "rhcertification-9": ["cpe:/a:redhat:certifications:1::el9"],
}


def cpe_lookup(product_stream_name: str) -> list[str]:
    """Temporary cpe fixup"""
    return supported_stream_cpes.get(product_stream_name, [])
