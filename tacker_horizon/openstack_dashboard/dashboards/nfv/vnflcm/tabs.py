# Copyright (C) 2024 Fujitsu
# All Rights Reserved.
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


from django.utils.translation import gettext_lazy as _

from horizon import exceptions
from horizon import tabs
from horizon import utils as horizon_utils

from tacker_horizon.openstack_dashboard import api
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnflcm import tables
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnflcmopocc \
    import tabs as opocc_tab


class VnfLcmItem(object):
    def __init__(self, vnf_id, vnf_instance_name, instantiation_state,
                 vnf_provider, vnf_software_version, vnf_product_name,
                 vnfd_id):
        self.id = vnf_id
        self.name = vnf_id
        self.vnf_instance_name = vnf_instance_name
        self.instantiation_state = instantiation_state
        self.vnf_provider = vnf_provider
        self.vnf_software_version = vnf_software_version
        self.vnf_product_name = vnf_product_name
        self.vnfd_id = vnfd_id


class VnfLcmTab(tabs.TableTab):
    name = _("VNFLCM tab")
    slug = "vnflcm_tab"
    table_classes = (tables.VnfLcmTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_prev_data(self, table):
        return self._has_prev

    def has_more_data(self, table):
        return self._has_more

    def get_vnflcm_data(self):
        try:
            self._has_prev = False
            page_size = horizon_utils.functions.get_page_size(self.request)
            marker = self.request.GET.get(
                "vnflcm_marker", None)
            prev_marker = self.request.GET.get(
                "prev_vnflcm_marker", None)
            vnf_instances = api.tacker.list_vnf_instances(self.request)
            if marker is not None or prev_marker is not None:
                for i, instance in enumerate(vnf_instances):
                    if instance["id"] == marker and i < len(vnf_instances) - 1:
                        vnf_instances = vnf_instances[i + 1:]
                        self._has_prev = True
                        break
                    if instance["id"] == prev_marker and i > page_size:
                        vnf_instances = vnf_instances[i - page_size:]
                        self._has_prev = True
                        break

            if len(vnf_instances) > page_size:
                self._has_more = True
            else:
                self._has_more = False

            rows = []
            for i, instance in enumerate(vnf_instances):
                if i >= page_size:
                    break
                item = VnfLcmItem(
                    vnf_id=instance.get('id', ''),
                    vnf_instance_name=instance.get('vnfInstanceName', ''),
                    instantiation_state=instance.get(
                        'instantiationState', ''),
                    vnf_provider=instance.get('vnfProvider', ''),
                    vnf_software_version=instance.get(
                        'vnfSoftwareVersion', ''),
                    vnf_product_name=instance.get('vnfProductName', ''),
                    vnfd_id=instance.get('vnfdId', ''))
                rows.append(item)
            return rows
        except Exception:
            self._has_more = False
            error_message = _('Failed to get VNF Instances.')
            exceptions.handle(self.request, error_message)

            return []


class VnfLcmTabs(tabs.TabGroup):
    slug = "vnflcm_tabs"
    tabs = (VnfLcmTab,)
    sticky = True


class VnfLcmOpOccItem(object):
    def __init__(self, id, operation_state, vnf_instance_id, operation):
        self.id = id
        self.operation_state = operation_state
        self.vnf_instance_id = vnf_instance_id
        self.operation = operation


class VnfLcmDetailTab(tabs.Tab):
    name = _("VNF Instance Detail Tab")
    slug = "vnflcm_detail_tab"
    template_name = "nfv/vnflcm/vnflcm_detail.html"

    def get_context_data(self, request):
        return {'vnflcm': self.tab_group.kwargs['vnflcm']}


class VnfLcmDetailTabs(tabs.TabGroup):
    slug = "vnflcm_detail_tabs"
    tabs = (VnfLcmDetailTab, opocc_tab.VnfLcmOpOccTab,)
    sticky = True
