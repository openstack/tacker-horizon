# Copyright 2015 Brocade Communications System, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from oslo_log import log as logging
from oslo_utils import strutils
from tackerclient.v1_0 import client as tacker_client

from horizon.utils.memoized import memoized  # noqa
from openstack_dashboard.api import base
from openstack_dashboard.contrib.developer.profiler import api as profiler


LOG = logging.getLogger(__name__)

SUPPORTED_VIM_TYPES = (
    ('openstack', 'OpenStack'),
    ('kubernetes', 'Kubernetes')
)

AUTH_METHODS = (
    ('basic', _('Basic')),
    ('bearer_token', _('Bearer Token'))
)

CERT_TRUE_TYPE = 'True'
CERT_FALSE_TYPE = 'False'
CERT_VERIFY_TYPES = (
    (CERT_TRUE_TYPE, _("True")),
    (CERT_FALSE_TYPE, _("False"))
)


@memoized
def tackerclient(request, api_version="1"):
    insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
    cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', None)
    c = tacker_client.Client(
        api_version=api_version,
        token=request.user.token.id,
        auth_url=base.url_for(request, 'identity'),
        endpoint_url=base.url_for(request, 'nfv-orchestration'),
        insecure=insecure, ca_cert=cacert)
    return c


@profiler.trace
def vnf_list(request, **params):
    LOG.debug("vnf_list(): params=%s", params)
    vnfs = tackerclient(request).list_vnfs(**params).get('vnfs')
    return vnfs


@profiler.trace
def vnfd_list(request, **params):
    LOG.debug("vnfd_list(): params=%s", params)
    vnfds = tackerclient(request).list_vnfds(**params).get('vnfds')
    return vnfds


@profiler.trace
def create_vnfd(request, tosca_body=None, **params):
    LOG.debug("create_vnfd(): params=%s", params)
    vnfd_instance = tackerclient(request).create_vnfd(body=tosca_body)
    return vnfd_instance


@profiler.trace
def create_vnf(request, vnf_arg, **params):
    LOG.debug("create_vnf(): vnf_arg=%s", str(vnf_arg))
    vnf_instance = tackerclient(request).create_vnf(body=vnf_arg)
    return vnf_instance


@profiler.trace
def get_vnfd(request, vnfd_id):
    LOG.debug("vnfd_get(): vnfd_id=%s", str(vnfd_id))
    vnfd = tackerclient(request).show_vnfd(vnfd_id)
    return vnfd


@profiler.trace
def get_vnf(request, vnf_id):
    LOG.debug("vnf_get(): vnf_id=%s", str(vnf_id))
    vnf_instance = tackerclient(request).show_vnf(vnf_id)
    return vnf_instance


@profiler.trace
def delete_vnf(request, vnf_id):
    LOG.debug("delete_vnf():vnf_id=%s", str(vnf_id))
    tackerclient(request).delete_vnf(vnf_id)


@profiler.trace
def delete_vnfd(request, vnfd_id):
    LOG.debug("delete_vnfd():vnfd_id=%s", str(vnfd_id))
    tackerclient(request).delete_vnfd(vnfd_id)


@profiler.trace
def create_vim(request, vim_arg):
    LOG.debug("create_vim(): vim_arg=%s", strutils.mask_password(vim_arg))
    vim_instance = tackerclient(request).create_vim(body=vim_arg)
    return vim_instance


@profiler.trace
def get_vim(request, vim_id):
    LOG.debug("vim_get(): vim_id=%s", str(vim_id))
    vim_instance = tackerclient(request).show_vim(vim_id)
    return vim_instance


@profiler.trace
def delete_vim(request, vim_id):
    LOG.debug("delete_vim():vim_id=%s", str(vim_id))
    tackerclient(request).delete_vim(vim_id)


@profiler.trace
def vim_list(request, **params):
    LOG.debug("vim_list(): params=%s", params)
    vims = tackerclient(request).list_vims(**params).get('vims')
    return vims


@profiler.trace
def events_list(request, resource_id):
    params = {'resource_id': resource_id}
    events = tackerclient(request).list_events(**params).get('events')
    LOG.debug("events_list() params=%s events=%s l=%s", params, events,
              len(events))
    return events


@profiler.trace
def vnffg_list(request, **params):
    LOG.debug("vnffg_list(): params=%s", params)
    vnffgs = tackerclient(request).list_vnffgs(**params).get('vnffgs')
    return vnffgs


@profiler.trace
def vnffgd_list(request, **params):
    LOG.debug("vnffgd_list(): params=%s", params)
    vnffgds = tackerclient(request).list_vnffgds(**params).get('vnffgds')
    return vnffgds


@profiler.trace
def create_vnffgd(request, tosca_body=None, **params):
    LOG.debug("create_vnffgd(): params=%s", params)
    vnffgd_instance = tackerclient(request).create_vnffgd(body=tosca_body)
    return vnffgd_instance


@profiler.trace
def create_vnffg(request, vnffg_arg, **params):
    LOG.debug("create_vnffg(): vnf_arg=%s", str(vnffg_arg))
    vnffg_instance = tackerclient(request).create_vnffg(body=vnffg_arg)
    return vnffg_instance


@profiler.trace
def get_vnffgd(request, vnffgd_id):
    LOG.debug("vnffgd_get(): vnffgd_id=%s", str(vnffgd_id))
    vnffgd = tackerclient(request).show_vnffgd(vnffgd_id)
    return vnffgd


@profiler.trace
def get_vnffg(request, vnffg_id):
    LOG.debug("vnffg_get(): vnffg_id=%s", str(vnffg_id))
    vnffg_instance = tackerclient(request).show_vnffg(vnffg_id)
    return vnffg_instance


@profiler.trace
def delete_vnffg(request, vnffg_id):
    LOG.debug("delete_vnffg():vnffg_id=%s", str(vnffg_id))
    tackerclient(request).delete_vnffg(vnffg_id)


@profiler.trace
def delete_vnffgd(request, vnffgd_id):
    LOG.debug("delete_vnffgd():vnffgd_id=%s", str(vnffgd_id))
    tackerclient(request).delete_vnffgd(vnffgd_id)


@profiler.trace
def create_nsd(request, tosca_body=None, **params):
    LOG.debug("create_nsd(): params=%s", params)
    nsd_instance = tackerclient(request).create_nsd(body=tosca_body)
    return nsd_instance


@profiler.trace
def nsd_list(request, **params):
    LOG.debug("nsd_list(): params=%s", params)
    nsds = tackerclient(request).list_nsds(**params).get('nsds')
    return nsds


@profiler.trace
def get_nsd(request, nsd_id):
    LOG.debug("nsd_get(): nsd_id=%s", str(nsd_id))
    nsd = tackerclient(request).show_nsd(nsd_id)
    return nsd


@profiler.trace
def delete_nsd(request, nsd_id):
    LOG.debug("delete_nsd():nsd_id=%s", str(nsd_id))
    tackerclient(request).delete_nsd(nsd_id)


@profiler.trace
def get_ns(request, ns_id):
    LOG.debug("ns_get(): ns_id=%s", str(ns_id))
    ns_instance = tackerclient(request).show_ns(ns_id)
    return ns_instance


@profiler.trace
def delete_ns(request, ns_id):
    LOG.debug("delete_ns():ns_id=%s", str(ns_id))
    tackerclient(request).delete_ns(ns_id)


@profiler.trace
def ns_list(request, **params):
    LOG.debug("ns_list(): params=%s", params)
    nss = tackerclient(request).list_nss(**params).get('nss')
    return nss


@profiler.trace
def create_ns(request, ns_arg, **params):
    LOG.debug("create_ns(): ns_arg=%s", str(ns_arg))
    ns_instance = tackerclient(request).create_ns(body=ns_arg)
    return ns_instance


# VNF Packages v1
@profiler.trace
def create_vnf_package(request, body):
    LOG.debug("create_vnf_package(): body=%s", body)
    vnf_package = tackerclient(request).create_vnf_package(body=body)
    return vnf_package


@profiler.trace
def list_vnf_packages(request, **params):
    LOG.debug("list_vnf_packages(): params=%s", params)
    vnf_packages = tackerclient(request).list_vnf_packages(**params).get(
        'vnf_packages')
    return vnf_packages


@profiler.trace
def get_vnf_package(request, vnf_pkg_id):
    LOG.debug("get_vnf_package(): vnf_pkg_id=%s", vnf_pkg_id)
    vnf_package = tackerclient(request).show_vnf_package(vnf_pkg_id)
    return vnf_package


@profiler.trace
def delete_vnf_package(request, vnf_pkg_id):
    LOG.debug("delete_vnf_package(): vnf_pkg_id=%s", vnf_pkg_id)
    result = tackerclient(request).delete_vnf_package(vnf_pkg_id)
    return result


@profiler.trace
def upload_vnf_package(request, vnf_pkg_id, file_data=None, **params):
    LOG.debug("upload_vnf_package(): vnf_pkg_id=%s, params=%s",
              vnf_pkg_id, params)
    vnf_package = tackerclient(request).upload_vnf_package(
        vnf_pkg_id, file_data=file_data, **params)
    return vnf_package


@profiler.trace
def update_vnf_package(request, vnf_pkg_id, body):
    LOG.debug("update_vnf_package(): vnf_pkg_id=%s, body=%s",
              vnf_pkg_id, body)
    updated_values = tackerclient(request).update_vnf_package(
        vnf_pkg_id, body=body)
    return updated_values


@profiler.trace
def fetch_vnf_package(request, vnf_pkg_id):
    LOG.debug("fetch_vnf_package(): vnf_pkg_id=%s", vnf_pkg_id)
    vnf_package_file = tackerclient(request).download_vnf_package(vnf_pkg_id)
    return vnf_package_file


# VNF LCM v2
@profiler.trace
def create_vnf_instance(request, body):
    LOG.debug("create_vnf_instance(): body=%s", body)
    vnf_instance = (tackerclient(request, api_version="2")
                    .create_vnf_instance(body=body))
    return vnf_instance


@profiler.trace
def get_vnf_instance(request, vnf_instance_id):
    LOG.debug("get_vnf_instance(): vnf_instance_id=%s", vnf_instance_id)
    vnf_instance = (tackerclient(request, api_version="2")
                    .show_vnf_instance(vnf_instance_id))
    return vnf_instance


@profiler.trace
def list_vnf_instances(request, **params):
    LOG.debug("list_vnf_instances(): params=%s", params)
    vnf_instances = (tackerclient(request, api_version="2")
                     .list_vnf_instances(**params))
    return vnf_instances


@profiler.trace
def delete_vnf_instance(request, vnf_instance_id):
    LOG.debug("delete_vnf_instance(): vnf_instance_id=%s", vnf_instance_id)
    result = (tackerclient(request, api_version="2")
              .delete_vnf_instance(vnf_instance_id))
    return result


@profiler.trace
def instantiate_vnf_instance(request, vnf_instance_id, body):
    LOG.debug("instantiate_vnf_instance(): vnf_instance_id=%s, body=%s",
              vnf_instance_id, body)
    result = (tackerclient(request, api_version="2")
              .instantiate_vnf_instance(vnf_instance_id, body=body))
    return result


@profiler.trace
def terminate_vnf_instance(request, vnf_instance_id, body):
    LOG.debug("terminate_vnf_instance(): vnf_instance_id=%s, body=%s",
              vnf_instance_id, body)
    result = (tackerclient(request, api_version="2")
              .terminate_vnf_instance(vnf_instance_id, body=body))
    return result


@profiler.trace
def heal_vnf_instance(request, vnf_instance_id, body):
    LOG.debug("heal_vnf_instance(): vnf_instance_id=%s, body=%s",
              vnf_instance_id, body)
    result = (tackerclient(request, api_version="2")
              .heal_vnf_instance(vnf_instance_id, body=body))
    return result


@profiler.trace
def update_vnf_instance(request, vnf_instance_id, body):
    LOG.debug("update_vnf_instance(): vnf_instance_id=%s, body=%s",
              vnf_instance_id, body)
    result = (tackerclient(request, api_version="2")
              .update_vnf_instance(vnf_instance_id, body=body))
    return result


@profiler.trace
def scale_vnf_instance(request, vnf_instance_id, body):
    LOG.debug("scale_vnf_instance(): vnf_instance_id=%s, body=%s",
              vnf_instance_id, body)
    result = (tackerclient(request, api_version="2")
              .scale_vnf_instance(vnf_instance_id, body=body))
    return result


@profiler.trace
def change_ext_conn_vnf_instance(request, vnf_instance_id, body):
    LOG.debug("change_ext_conn_vnf_instance(): vnf_instance_id=%s, body=%s",
              vnf_instance_id, body)
    result = (tackerclient(request, api_version="2")
              .change_ext_conn_vnf_instance(vnf_instance_id, body=body))
    return result


@profiler.trace
def change_vnfpkg_vnf_instance(request, vnf_instance_id, body):
    LOG.debug("change_vnfpkg_vnf_instance(): vnf_instance_id=%s, body=%s",
              vnf_instance_id, body)
    result = (tackerclient(request, api_version="2")
              .change_vnfpkg_vnf_instance(vnf_instance_id, body=body))
    return result


@profiler.trace
def list_vnf_lcm_op_occs(request, **params):
    LOG.debug("list_vnf_lcm_op_occs(): params=%s", params)
    op_occs = (tackerclient(request, api_version="2")
               .list_vnf_lcm_op_occs(**params))
    return op_occs


@profiler.trace
def get_vnf_lcm_op_occ(request, op_occ_id):
    LOG.debug("get_vnf_lcm_op_occ(): op_occ_id=%s", op_occ_id)
    op_occ = (tackerclient(request, api_version="2")
              .show_vnf_lcm_op_occs(op_occ_id))
    return op_occ


@profiler.trace
def rollback_vnf_lcm_op_occ(request, op_occ_id):
    LOG.debug("rollback_vnf_lcm_op_occ(): op_occ_id=%s", op_occ_id)
    result = (tackerclient(request, api_version="2")
              .rollback_vnf_instance(op_occ_id))
    return result


@profiler.trace
def retry_vnf_lcm_op_occ(request, op_occ_id):
    LOG.debug("retry_vnf_lcm_op_occ(): op_occ_id=%s", op_occ_id)
    result = (tackerclient(request, api_version="2")
              .retry_vnf_instance(op_occ_id))
    return result


@profiler.trace
def fail_vnf_lcm_op_occ(request, op_occ_id):
    LOG.debug("fail_vnf_lcm_op_occs(): op_occ_id=%s", op_occ_id)
    result = (tackerclient(request, api_version="2")
              .fail_vnf_instance(op_occ_id))
    return result


@profiler.trace
def list_vnf_lcm_subscriptions(request, **params):
    LOG.debug("list_vnf_lcm_subscriptions(): params=%s", params)
    subscriptions = (tackerclient(request, api_version="2")
                     .list_lccn_subscriptions(**params))
    return subscriptions


@profiler.trace
def get_vnf_lcm_subscription(request, subsc_id):
    LOG.debug("get_vnf_lcm_subscription(): subsc_id=%s", subsc_id)
    subscription = (tackerclient(request, api_version="2")
                    .show_lccn_subscription(subsc_id))
    return subscription


@profiler.trace
def delete_vnf_lcm_subscription(request, subsc_id):
    LOG.debug("delete_vnf_lcm_subscription(): subsc_id=%s", subsc_id)
    result = (tackerclient(request, api_version="2")
              .delete_lccn_subscription(subsc_id))
    return result


@profiler.trace
def create_vnf_lcm_subscription(request, param):
    LOG.debug("create_vnf_lcm_subscription(): param=%s", param)
    subscription = (tackerclient(request, api_version="2")
                    .create_lccn_subscription(body=param))
    return subscription


# VNF FM v1
@profiler.trace
def list_fm_alarms(request, **params):
    LOG.debug("list_fm_alarms(): params=%s", params)
    fm_alarms = tackerclient(request).list_vnf_fm_alarms(**params).get(
        'vnf_fm_alarms')
    return fm_alarms


@profiler.trace
def get_fm_alarm(request, alarm_id):
    LOG.debug("get_fm_alarm(): alarm_id=%s", alarm_id)
    fm_alarm = tackerclient(request).show_vnf_fm_alarm(alarm_id)
    return fm_alarm


@profiler.trace
def update_fm_alarm(request, alarm_id, body):
    LOG.debug("update_fm_alarm(): alarm_id=%s, body=%s", alarm_id, body)
    updated_values = tackerclient(request).update_vnf_fm_alarm(
        alarm_id, body=body)
    return updated_values


@profiler.trace
def create_fm_subscription(request, body):
    LOG.debug("create_fm_subscription(): body=%s", body)
    fm_subscription = tackerclient(request).create_vnf_fm_sub(body=body)
    return fm_subscription


@profiler.trace
def list_fm_subscriptions(request, **params):
    LOG.debug("list_fm_subscriptions(): params=%s", params)
    fm_subscriptions = tackerclient(request).list_vnf_fm_subs(**params).get(
        'vnf_fm_subs')
    return fm_subscriptions


@profiler.trace
def get_fm_subscription(request, subsc_id):
    LOG.debug("get_fm_subscription(): subsc_id=%s", subsc_id)
    fm_subscription = tackerclient(request).show_vnf_fm_sub(subsc_id)
    return fm_subscription


@profiler.trace
def delete_fm_subscription(request, subsc_id):
    LOG.debug("delete_fm_subscription(): subsc_id=%s", subsc_id)
    result = tackerclient(request).delete_vnf_fm_sub(subsc_id)
    return result


# VNF PM v2
@profiler.trace
def create_pm_job(request, body):
    LOG.debug("create_pm_job(): body=%s", body)
    pm_job = (tackerclient(request, api_version="2")
              .create_vnf_pm_job(body=body))
    return pm_job


@profiler.trace
def list_pm_jobs(request, **params):
    LOG.debug("list_pm_jobs(): params=%s", params)
    pm_jobs = (tackerclient(request, api_version="2")
               .list_vnf_pm_jobs(**params).get('vnf_pm_jobs'))
    return pm_jobs


@profiler.trace
def get_pm_job(request, pm_job_id):
    LOG.debug("get_pm_job(): pm_job_id=%s", pm_job_id)
    pm_job = tackerclient(request, api_version="2").show_vnf_pm_job(pm_job_id)
    return pm_job


@profiler.trace
def update_pm_job(request, pm_job_id, body):
    LOG.debug("update_pm_job(): pm_job_id=%s, body=%s", pm_job_id, body)
    updated_values = (tackerclient(request, api_version="2")
                      .update_vnf_pm_job(pm_job_id, body=body))
    return updated_values


@profiler.trace
def delete_pm_job(request, pm_job_id):
    LOG.debug("delete_pm_job(): pm_job_id=%s", pm_job_id)
    result = (tackerclient(request, api_version="2")
              .delete_vnf_pm_job(pm_job_id))
    return result


@profiler.trace
def get_pm_report(request, pm_job_id, pm_report_id):
    LOG.debug("get_pm_report(): pm_job_id=%s, pm_report_id=%s",
              pm_job_id, pm_report_id)
    pm_report = (tackerclient(request, api_version="2")
                 .show_vnf_pm_report(pm_job_id, pm_report_id))
    return pm_report


@profiler.trace
def create_pm_threshold(request, body):
    LOG.debug("create_pm_threshold(): body=%s", body)
    pm_threshold = (tackerclient(request, api_version="2")
                    .create_vnf_pm_threshold(body=body))
    return pm_threshold


@profiler.trace
def list_pm_thresholds(request, **params):
    LOG.debug("list_pm_thresholds(): params=%s", params)
    pm_thresholds = (tackerclient(request, api_version="2")
                     .list_vnf_pm_thresholds(**params)
                     .get('vnf_pm_thresholds'))
    return pm_thresholds


@profiler.trace
def get_pm_threshold(request, pm_threshold_id):
    LOG.debug("get_pm_threshold(): pm_threshold_id=%s", pm_threshold_id)
    pm_threshold = (tackerclient(request, api_version="2")
                    .show_vnf_pm_threshold(pm_threshold_id))
    return pm_threshold


@profiler.trace
def update_pm_threshold(request, pm_threshold_id, body):
    LOG.debug("update_pm_threshold(): pm_threshold_id=%s, body=%s",
              pm_threshold_id, body)
    updated_values = (tackerclient(request, api_version="2")
                      .update_vnf_pm_threshold(pm_threshold_id, body=body))
    return updated_values


@profiler.trace
def delete_pm_threshold(request, pm_threshold_id):
    LOG.debug("delete_pm_threshold(): pm_threshold_id=%s", pm_threshold_id)
    result = (tackerclient(request, api_version="2")
              .delete_vnf_pm_threshold(pm_threshold_id))
    return result
