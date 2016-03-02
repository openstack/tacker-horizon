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

from __future__ import absolute_import

import logging

from django.conf import settings
from tackerclient.v1_0 import client as tacker_client

from horizon.utils.memoized import memoized  # noqa
from openstack_dashboard.api import base


LOG = logging.getLogger(__name__)


@memoized
def tackerclient(request):
    insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
    cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', None)
    c = tacker_client.Client(
        token=request.user.token.id,
        auth_url=base.url_for(request, 'identity'),
        endpoint_url=base.url_for(request, 'nfv-orchestration'),
        insecure=insecure, ca_cert=cacert)
    return c


def vnf_list(request, **params):
    LOG.debug("vnf_list(): params=%s", params)
    vnfs = tackerclient(request).list_vnfs(**params).get('vnfs')
    return vnfs


def vnfd_list(request, **params):
    LOG.debug("vnfd_list(): params=%s", params)
    vnfds = tackerclient(request).list_vnfds(**params).get('vnfds')
    return vnfds


def create_vnfd(request, tosca_body=None, **params):
    LOG.debug("create_vnfd(): params=%s", params)
    vnfd_instance = tackerclient(request).create_vnfd(body=tosca_body)
    return vnfd_instance


def create_vnf(request, vnf_arg, **params):
    LOG.debug("create_vnf(): vnf_arg=%s", str(vnf_arg))
    vnf_instance = tackerclient(request).create_vnf(body=vnf_arg)
    return vnf_instance


def get_vnfd(request, vnfd_id):
    LOG.debug("vnfd_get(): vnfd_id=%s", str(vnfd_id))
    vnfd = tackerclient(request).show_vnfd(vnfd_id)
    return vnfd


def get_vnf(request, vnf_id):
    LOG.debug("vnf_get(): vnf_id=%s", str(vnf_id))
    vnf_instance = tackerclient(request).show_vnf(vnf_id)
    return vnf_instance


def delete_vnf(request, vnf_id):
    LOG.debug("delete_vnf():vnf_id=%s", str(vnf_id))
    tackerclient(request).delete_vnf(vnf_id)


def delete_vnfd(request, vnfd_id):
    LOG.debug("delete_vnfd():vnfd_id=%s", str(vnfd_id))
    tackerclient(request).delete_vnfd(vnfd_id)


def create_vim(request, vim_arg):
    LOG.debug("create_vim(): vim_arg=%s", str(vim_arg))
    vim_instance = tackerclient(request).create_vim(body=vim_arg)
    return vim_instance


def get_vim(request, vim_id):
    LOG.debug("vim_get(): vim_id=%s", str(vim_id))
    vim_instance = tackerclient(request).show_vim(vim_id)
    return vim_instance


def delete_vim(request, vim_id):
    LOG.debug("delete_vim():vim_id=%s", str(vim_id))
    tackerclient(request).delete_vim(vim_id)


def vim_list(request, **params):
    LOG.debug("vim_list(): params=%s", params)
    vims = tackerclient(request).list_vims(**params).get('vims')
    return vims
