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
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfcatalog import tables


class VNFCatalogItem(object):
    def __init__(self, name, description, service_types, vnfd_id):
        self.id = vnfd_id
        self.name = name
        self.description = description
        self.service_types = service_types


class VNFCatalogTab(tabs.TableTab):
    name = _("VNFCatalog Tab")
    slug = "vnfcatalog_tab"
    table_classes = (tables.VNFCatalogTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_vnfcatalog_data(self):
        try:
            catalogs = []
            vnfds = api.tacker.vnfd_list(self.request,
                                         template_source="onboarded")

            if len(vnfds) > horizon_utils.functions.get_page_size(
                    self.request):
                self._has_more = True
            else:
                self._has_more = False

            for vnfd in vnfds:
                s_types = [s_type for s_type in vnfd['service_types']]
                s_types_string = ""
                if len(s_types) > 0:
                    s_types_string = ', '.join(
                        [str(item) for item in s_types])
                item = VNFCatalogItem(vnfd['name'],
                                      vnfd['description'],
                                      s_types_string, vnfd['id'])
                catalogs.append(item)
            return catalogs
        except Exception:
            self._has_more = False
            error_message = _('Unable to get vnf catalogs')
            exceptions.handle(self.request, error_message)

            return []


class VNFCatalogTabs(tabs.TabGroup):
    slug = "vnfcatalog_tabs"
    tabs = (VNFCatalogTab,)
    sticky = True


class TemplateTab(tabs.Tab):
    name = _("Template")
    slug = "template"
    template_name = ("nfv/vnfcatalog/template.html")

    def get_context_data(self, request):
        return {'vnfd': self.tab_group.kwargs['vnfd']}


class VNFDEventsTab(tabs.TableTab):
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
                                            self.tab_group.kwargs['vnfd_id'])

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


class VNFDDetailTabs(tabs.TabGroup):
    slug = "VNFD_details"
    tabs = (TemplateTab, VNFDEventsTab)
    sticky = True
