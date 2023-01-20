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

from django.utils.translation import gettext_lazy as _
from horizon import exceptions
from horizon import tabs
from horizon import utils as horizon_utils

from tacker_horizon.openstack_dashboard import api
from tacker_horizon.openstack_dashboard.dashboards.nfv import utils
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfmanager import tables


class VNFManagerTab(tabs.TableTab):
    name = _("VNFManager Tab")
    slug = "vnfmanager_tab"
    table_classes = (tables.VNFManagerTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_vnfmanager_data(self):
        try:
            tables.VNFManagerItemList.clear_list()
            vnfs = api.tacker.vnf_list(self.request)

            if len(vnfs) > horizon_utils.functions.get_page_size(
                    self.request):
                self._has_more = True
            else:
                self._has_more = False

            for vnf in vnfs:
                try:
                    vnf_services_str = vnf['attributes']['service_type']
                except KeyError:
                    vnf_services_str = ""
                try:
                    vnf_desc_str = vnf['description']
                except KeyError:
                    vnf_desc_str = ""

                vim = vnf['placement_attr'].get('vim_name', '')
                obj = tables.VNFManagerItem(
                    vnf['name'],
                    vnf_desc_str,
                    vnf_services_str,
                    vim,
                    vnf['status'],
                    vnf['status'],
                    vnf['id'],
                    vnf['error_reason'])
                tables.VNFManagerItemList.add_item(obj)
            return tables.VNFManagerItemList.VNFLIST_P
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []


class VNFManagerTabs(tabs.TabGroup):
    slug = "vnfmanager_tabs"
    tabs = (VNFManagerTab,)
    sticky = True


class VDUDetailTab(tabs.Tab):
    name = _("VDU Detail")
    slug = "VDU_Details"
    template_name = "nfv/vnfmanager/vdu_details.html"

    def get_context_data(self, request):
        return {'vnf': self.tab_group.kwargs['vnf']}


class VNFEventsTab(tabs.TableTab):
    name = _("Events Tab")
    slug = "events_tab"
    table_classes = (utils.EventsTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_events_data(self):
        try:
            utils.EventItemList.clear_list()
            events = api.tacker.events_list(self.request,
                                            self.tab_group.kwargs['vnf_id'])

            if len(events) > horizon_utils.functions.get_page_size(
                    self.request):
                self._has_more = True
            else:
                self._has_more = False

            for event in events:
                evt_obj = utils.EventItem(
                    event['id'], event['resource_state'],
                    event['event_type'],
                    event['timestamp'],
                    event['event_details'])
                utils.EventItemList.add_item(evt_obj)
            return utils.EventItemList.EVTLIST_P
        except Exception:
            self._has_more = False
            error_message = _('Unable to get events.')
            exceptions.handle(self.request, error_message)
            return []


class VNFDetailsTabs(tabs.TabGroup):
    slug = "VNF_details"
    tabs = (VDUDetailTab, VNFEventsTab)
    sticky = True
