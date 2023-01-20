# Copyright 2016 Brocade Communications System, Inc.
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
from tacker_horizon.openstack_dashboard.dashboards.nfv import utils  # noqa
from tacker_horizon.openstack_dashboard.dashboards.nfv.vim import tables


class VIMItem(object):
    def __init__(self, name, description, is_default, regions, vim_id,
                 auth_url, user, project, status, vim_type):
        self.id = vim_id
        self.name = name
        self.description = description
        self.is_default = is_default
        self.regions = regions
        self.auth_url = auth_url
        self.user = user
        self.project = project
        self.status = status
        self.type = vim_type


class VIMTab(tabs.TableTab):
    name = _("VIM Tab")
    slug = "vim_tab"
    table_classes = (tables.VIMTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_vim_data(self):
        try:
            instances = []
            vims = api.tacker.vim_list(self.request)

            if len(vims) > horizon_utils.functions.get_page_size(
                    self.request):
                self._has_more = True
            else:
                self._has_more = False

            for vim in vims:
                auth_cred = vim['auth_cred']
                placement_attr = vim['placement_attr']
                vim_regions = ','.join(placement_attr['regions'])
                user = "<Bearer token>"
                if 'bearer_token' not in auth_cred.keys():
                    user = auth_cred['username'] if auth_cred[
                        'username'] else auth_cred['user_id']
                project_info = vim['vim_project']
                project = project_info['name'] if project_info[
                    'name'] else project_info['id']
                status = vim["status"]
                is_default = vim['is_default']
                vim_type = vim["type"]
                item = VIMItem(name=vim.get('name', ''),
                               description=vim.get('description', ''),
                               is_default=is_default,
                               regions=vim_regions,
                               vim_id=vim.get('id', ''),
                               auth_url=vim.get('auth_url', ''),
                               user=user, project=project, status=status,
                               vim_type=vim_type)
                instances.append(item)
            return instances
        except Exception:
            self._has_more = False
            error_message = _('Unable to fetch vim list')
            exceptions.handle(self.request, error_message)

            return []


class VIMEventsTab(tabs.TableTab):
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
                                            self.tab_group.kwargs['vim_id'])

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


class VIMTabs(tabs.TabGroup):
    slug = "vim_tabs"
    tabs = (VIMTab,)
    sticky = True


class VIMDetailsTabs(tabs.TabGroup):
    slug = "VIM_details"
    tabs = (VIMEventsTab,)
    sticky = True
