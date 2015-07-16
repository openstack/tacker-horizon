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

import collections
import logging

import netaddr

from django.conf import settings
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _
from neutronclient.common import exceptions as neutron_exc
from neutronclient.v2_0 import client as neutron_client
from tackerclient.v1_0 import client as tacker_client

from horizon import messages
from horizon.utils.memoized import memoized  # noqa
from openstack_dashboard.api import base
from openstack_dashboard.api import network_base
from openstack_dashboard.api import nova
from openstack_dashboard import policy


LOG = logging.getLogger(__name__)


@memoized
def tackerclient(request):
    insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
    cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', None)
    c = tacker_client.Client(token=request.user.token.id,
                             auth_url=base.url_for(request, 'identity'),
                             endpoint_url=base.url_for(request, 'servicevm'),
                             insecure=insecure, ca_cert=cacert)
    return c


def vnf_list(request, **params):
    LOG.debug("vnf_list(): params=%s", params)
    vnfs = tackerclient(request).list_vnfs(**params).get('vnfs')
    print "API.Tacker VNFs::" + str(vnfs)
    return vnfs


def vnfd_list(request, **params):
    LOG.debug("vnfd_list(): params=%s", params)
    vnfds = tackerclient(request).list_vnfds(**params).get('vnfds')
    print "API.Tacker VNFDs:" + str(vnfds)
    return vnfds


def create_vnfd(request, tosca_body=None, **params):
    LOG.debug("create_vnfd(): params=%s", params)
    vnfd_instance = tackerclient(request).create_vnfd(body=tosca_body)
    print "API.Tacker VNFD Instance: " + str(vnfd_instance)
    return vnfd_instance


def create_vnf(request, vnf_arg, **params):
    LOG.debug("create_vnf(): vnf_arg=%s", str(vnf_arg))
    vnf_instance = tackerclient(request).create_vnf(body=vnf_arg)
    print "API.Tacker VNF Instance: " + str(vnf_instance)
    return vnf_instance


def get_vnf(request, vnf_id):
    LOG.debug("vnf_get(): vnf_id=%s", str(vnf_id))
    vnf_instance = tackerclient(request).show_vnf(vnf_id)
    print "API.Tacker Get VNF Instance: " + str(vnf_instance)
    return vnf_instance

def delete_vnf(request, vnf_id):
    LOG.debug("delete_vnf():vnf_id=%s",str(vnf_id))
    tackerclient(request).delete_vnf(vnf_id)

def delete_vnfd(request, vnfd_id):
    LOG.debug("delete_vnfd():vnfd_id=%s",str(vnfd_id))
    tackerclient(request).delete_vnfd(vnfd_id)