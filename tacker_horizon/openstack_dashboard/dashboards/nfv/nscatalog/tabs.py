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
from tacker_horizon.openstack_dashboard.dashboards.nfv.nscatalog import tables
from tacker_horizon.openstack_dashboard.dashboards.nfv import utils


class NSCatalogItem(object):
    def __init__(self, name, description, nsd_id):
        self.id = nsd_id
        self.name = name
        self.description = description


class NSCatalogTab(tabs.TableTab):
    name = _("NSCatalog Tab")
    slug = "nscatalog_tab"
    table_classes = (tables.NSCatalogTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_nscatalog_data(self):
        try:
            instances = []
            nsds = api.tacker.nsd_list(self.request)

            if len(nsds) > horizon_utils.functions.get_page_size(
                    self.request):
                self._has_more = True
            else:
                self._has_more = False

            for nsd in nsds:
                item = NSCatalogItem(nsd['name'],
                                     nsd['description'],
                                     nsd['id'])
                instances.append(item)
            return instances
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []


class NSCatalogTabs(tabs.TabGroup):
    slug = "nscatalog_tabs"
    tabs = (NSCatalogTab,)
    sticky = True


class TemplateTab(tabs.Tab):
    name = _("Template")
    slug = "template"
    template_name = ("nfv/nscatalog/template.html")

    def get_context_data(self, request):
        return {'nsd': self.tab_group.kwargs['nsd']}


class NSDEventsTab(tabs.TableTab):
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
                                            self.tab_group.kwargs['nsd_id'])

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


class NSDDetailTabs(tabs.TabGroup):
    slug = "NSD_details"
    tabs = (TemplateTab, NSDEventsTab)
    sticky = True
