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
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfpmthreshold \
    import tables


class VnfPmThresholdItem(object):
    def __init__(self, threshold_id, links, object_type):
        self.id = threshold_id
        self.name = threshold_id
        self.links = links
        self.object_type = object_type


class VnfPmThresholdTab(tabs.TableTab):
    name = _("VNFPMThreshold Tab")
    slug = "vnfpmthreshold_tab"
    table_classes = (tables.VnfPmThresholdTable,)
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def has_prev_data(self, table):
        return self._has_prev

    def has_more_data(self, table):
        return self._has_more

    def get_pmthreshold_data(self):
        try:
            self._has_prev = False
            page_size = horizon_utils.functions.get_page_size(self.request)
            marker = self.request.GET.get("vnfpmthreshold_marker", None)
            prev_marker = self.request.GET.get(
                "prev_vnfpmthreshold_marker", None)
            pmthresholds = api.tacker.list_pm_thresholds(self.request)

            if marker is not None or prev_marker is not None:
                for i, threshold in enumerate(pmthresholds):
                    if threshold["id"] == marker and i < len(pmthresholds) - 1:
                        pmthresholds = pmthresholds[i + 1:]
                        self._has_prev = True
                        break
                    if threshold["id"] == prev_marker and i > page_size:
                        pmthresholds = pmthresholds[i - page_size:]
                        self._has_prev = True
                        break

            if len(pmthresholds) > page_size:
                self._has_more = True
            else:
                self._has_more = False

            rows = []
            for i, threshold in enumerate(pmthresholds):
                if i >= page_size:
                    break
                item = VnfPmThresholdItem(threshold['id'],
                                          threshold['_links'],
                                          threshold['objectType'])
                rows.append(item)
            return rows
        except Exception:
            self._has_more = False
            error_message = _('Failed to get PM Thresholds.')
            exceptions.handle(self.request, error_message)
            return []


class VnfPmThresholdTabs(tabs.TabGroup):
    slug = "vnfpmthreshold_tabs"
    tabs = (VnfPmThresholdTab,)
    sticky = True


class VnfPmThresholdDetailTab(tabs.Tab):
    name = _("VNF PM Threshold")
    slug = "vnfpmthreshold_detail_tab"
    template_name = "nfv/vnfpmthreshold/pmthreshold_detail.html"

    def get_context_data(self, request):
        return {'pmthreshold': self.tab_group.kwargs['pmthreshold']}


class VnfPmThresholdDetailTabs(tabs.TabGroup):
    slug = "vnfpmthreshold_detail_tabs"
    tabs = (VnfPmThresholdDetailTab,)
    sticky = True
