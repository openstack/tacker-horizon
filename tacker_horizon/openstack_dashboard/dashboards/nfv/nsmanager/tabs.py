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
from tacker_horizon.openstack_dashboard.dashboards.nfv.nsmanager import tables
from tacker_horizon.openstack_dashboard.dashboards.nfv import utils


class NSManagerTab(tabs.TableTab):
    name = _("NSManager Tab")
    slug = "nsmanager_tab"
    table_classes = (tables.NSManagerTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_nsmanager_data(self):
        try:
            tables.NSManagerItemList.clear_list()
            nss = api.tacker.ns_list(self.request)

            if len(nss) > horizon_utils.functions.get_page_size(
                    self.request):
                self._has_more = True
            else:
                self._has_more = False

            for ns in nss:
                try:
                    ns_desc_str = ns['description']
                except KeyError:
                    ns_desc_str = ""

                vim = ns['vim_id']
                obj = tables.NSManagerItem(
                    ns['name'],
                    ns_desc_str,
                    vim,
                    ns['status'],
                    ns['id'],
                    ns['error_reason'])
                tables.NSManagerItemList.add_item(obj)
            return tables.NSManagerItemList.NSLIST_P
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []


class NSManagerTabs(tabs.TabGroup):
    slug = "nsmanager_tabs"
    tabs = (NSManagerTab,)
    sticky = True


class NSEventsTab(tabs.TableTab):
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
                                            self.tab_group.kwargs['ns_id'])

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


class NSDetailsTabs(tabs.TabGroup):
    slug = "NS_details"
    tabs = (NSEventsTab,)
    sticky = True
