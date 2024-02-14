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
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnflcmopocc \
    import tables


class VnfLcmOpOccItem(object):
    def __init__(self, opocc_id, operation_state, vnf_instance_id,
                 operation):
        self.id = opocc_id
        self.name = opocc_id
        self.operation_state = operation_state
        self.vnf_instance_id = vnf_instance_id
        self.operation = operation


class VnfLcmOpOccTab(tabs.TableTab):
    name = _("List LCM Operation Occurrences")
    slug = "vnflcmopocc_tab"
    table_classes = (tables.VnfLcmOpOccTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_prev_data(self, table):
        return self._has_prev

    def has_more_data(self, table):
        return self._has_more

    def get_vnflcmopocc_data(self):
        try:
            opoccs = []
            self._has_prev = False
            page_size = horizon_utils.functions.get_page_size(self.request)
            marker = self.request.GET.get(
                "opocc_marker", None)
            prev_marker = self.request.GET.get(
                "prev_opocc_marker", None)
            params = {}
            opocc_id = self.request.resolver_match.kwargs.get("id", None)
            if opocc_id:
                params["filter"] = "(eq,vnfInstanceId,{0})".format(opocc_id)
            opoccs = api.tacker.list_vnf_lcm_op_occs(self.request, **params)
            if marker is not None or prev_marker is not None:
                for i, opocc in enumerate(opoccs):
                    if opocc["id"] == marker and i < len(opoccs) - 1:
                        opoccs = opoccs[i + 1:]
                        self._has_prev = True
                        break
                    if opocc["id"] == prev_marker and i > page_size:
                        opoccs = opoccs[i - page_size:]
                        self._has_prev = True
                        break

            if len(opoccs) > page_size:
                self._has_more = True
            else:
                self._has_more = False

            rows = []
            for i, opocc in enumerate(opoccs):
                if i >= page_size:
                    break
                item = VnfLcmOpOccItem(
                    opocc_id=opocc.get('id', ''),
                    operation_state=opocc.get('operationState', ''),
                    vnf_instance_id=opocc.get('vnfInstanceId', ''),
                    operation=opocc.get('operation', ''))
                rows.append(item)
            return rows
        except Exception:
            self._has_more = False
            error_message = _('Failed to get VNF LCM operation occurrences.')
            exceptions.handle(self.request, error_message)

            return []


class VnfLcmOpOccTabs(tabs.TabGroup):
    slug = "vnflcmopocc_tabs"
    tabs = (VnfLcmOpOccTab,)
    sticky = True


class VnfOpOccDetailTab(tabs.Tab):
    name = _("LCM OP OCC Detail")
    slug = "vnflcmopocc_detail_tab"
    template_name = "nfv/vnflcmopocc/vnflcmopocc_detail.html"

    def get_context_data(self, request):
        return {'vnflcmopocc': self.tab_group.kwargs['vnflcmopocc']}


class VnfOpOccDetailTabs(tabs.TabGroup):
    slug = "vnflcmopocc_detail_tabs"
    tabs = (VnfOpOccDetailTab,)
    sticky = True
