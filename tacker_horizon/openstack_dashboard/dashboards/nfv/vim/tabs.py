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


from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from tacker_horizon.openstack_dashboard import api
from tacker_horizon.openstack_dashboard.dashboards.nfv.vim import tables


class VIMItem(object):
    def __init__(self, name, description, regions, vim_id, auth_url,
                 user, project):
        self.id = vim_id
        self.name = name
        self.description = description
        self.regions = regions
        self.auth_url = auth_url
        self.user = user
        self.project = project


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
            self._has_more = False
            instances = []
            vims = api.tacker.vim_list(self.request)
            for vim in vims:
                auth_cred = vim['auth_cred']
                placement_attr = vim['placement_attr']
                vim_regions = ','.join(placement_attr['regions'])
                user = auth_cred['username'] if auth_cred[
                    'username'] else auth_cred['user_id']
                project_info = vim['vim_project']
                project = project_info['name'] if project_info[
                    'name'] else project_info['id']
                item = VIMItem(name=vim.get('name', ''),
                               description=vim.get('description', ''),
                               regions=vim_regions,
                               vim_id=vim.get('id', ''),
                               auth_url=vim.get('auth_url', ''),
                               user=user, project=project)
                instances.append(item)
            return instances
        except Exception:
            self._has_more = False
            error_message = _('Unable to fetch vim list')
            exceptions.handle(self.request, error_message)

            return []


class VIMTabs(tabs.TabGroup):
    slug = "vim_tabs"
    tabs = (VIMTab,)
    sticky = True
