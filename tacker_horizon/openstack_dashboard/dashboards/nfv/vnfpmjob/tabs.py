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
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfpmjob \
    import tables


class VnfPmJobItem(object):
    def __init__(self, job_id, links, object_type):
        self.id = job_id
        self.name = job_id
        self.links = links
        self.object_type = object_type


class VnfPmJobTab(tabs.TableTab):
    name = _("VNFPMJob Tab")
    slug = "vnfpmjob_tab"
    table_classes = (tables.VnfPmJobTable,)
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def has_prev_data(self, table):
        return self._has_prev

    def has_more_data(self, table):
        return self._has_more

    def get_pmjob_data(self):
        try:
            self._has_prev = False
            page_size = horizon_utils.functions.get_page_size(self.request)
            marker = self.request.GET.get("vnfpmjob_marker", None)
            prev_marker = self.request.GET.get("prev_vnfpmjob_marker", None)
            pmjobs = api.tacker.list_pm_jobs(self.request)

            if marker is not None or prev_marker is not None:
                for i, pmjob in enumerate(pmjobs):
                    if pmjob["id"] == marker and i < len(pmjobs) - 1:
                        pmjobs = pmjobs[i + 1:]
                        self._has_prev = True
                        break
                    if pmjob["id"] == prev_marker and i > page_size:
                        pmjobs = pmjobs[i - page_size:]
                        self._has_prev = True
                        break

            if len(pmjobs) > page_size:
                self._has_more = True
            else:
                self._has_more = False

            rows = []
            for i, pmjob in enumerate(pmjobs):
                if i >= page_size:
                    break
                item = VnfPmJobItem(pmjob['id'],
                                    pmjob['_links'],
                                    pmjob['objectType'])
                rows.append(item)
            return rows
        except Exception:
            self._has_more = False
            error_message = _('Failed to get PM Jobs.')
            exceptions.handle(self.request, error_message)
            return []


class VnfPmJobTabs(tabs.TabGroup):
    slug = "vnfpmjob_tabs"
    tabs = (VnfPmJobTab,)
    sticky = True


class VnfPmJobDetailTab(tabs.Tab):
    name = _("VNF PM Job")
    slug = "vnfpmjob_detail_tab"
    template_name = "nfv/vnfpmjob/pmjob_detail.html"

    def get_context_data(self, request):
        return {'pmjob': self.tab_group.kwargs['pmjob']}


class VnfPmJobDetailTabs(tabs.TabGroup):
    slug = "vnfpmjob_detail_tabs"
    tabs = (VnfPmJobDetailTab,)
    sticky = True


class VnfPmJobReportDetailTab(tabs.Tab):
    name = _("PM Job Reports")
    slug = "vnfpmjob_report_detail_tab"
    template_name = "nfv/vnfpmjob/report_detail.html"

    def get_context_data(self, request):
        return {'report': self.tab_group.kwargs['report']}


class VnfPmJobReportDetailTabs(tabs.TabGroup):
    slug = "vnfpmjob_report_detail_tabs"
    tabs = (VnfPmJobReportDetailTab,)
    sticky = True
