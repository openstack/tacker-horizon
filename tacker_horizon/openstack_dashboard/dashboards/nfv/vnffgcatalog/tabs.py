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
import yaml

from horizon import exceptions
from horizon import tabs
from horizon import utils as horizon_utils

from tacker_horizon.openstack_dashboard import api
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnffgcatalog \
    import tables


class VNFFGCatalogItem(object):
    def __init__(self, name, description, vnffgd_id):
        self.id = vnffgd_id
        self.name = name
        self.description = description


class VNFFGCatalogTab(tabs.TableTab):
    name = _("VNFFGCatalog Tab")
    slug = "vnffgcatalog_tab"
    table_classes = (tables.VNFFGCatalogTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_vnffgcatalog_data(self):
        try:
            instances = []
            vnffgds = api.tacker.vnffgd_list(self.request)

            if len(vnffgds) > horizon_utils.functions.get_page_size(
                    self.request):
                self._has_more = True
            else:
                self._has_more = False

            for vnffgd in vnffgds:
                item = VNFFGCatalogItem(vnffgd['name'],
                                        vnffgd['description'],
                                        vnffgd['id'])
                instances.append(item)
            return instances
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)
            return []


class VNFFGCatalogTabs(tabs.TabGroup):
    slug = "vnffgcatalog_tabs"
    tabs = (VNFFGCatalogTab,)
    sticky = True


class TemplateTab(tabs.Tab):
    name = _("Template")
    slug = "template"
    template_name = ("nfv/vnffgcatalog/template.html")

    def get_context_data(self, request):
        vnffgd = self.tab_group.kwargs['vnffgd']
        vnffgd['template'] = yaml.safe_dump(vnffgd['template'],
                                            default_flow_style=False)
        return {'vnffgd': self.tab_group.kwargs['vnffgd']}


class VNFFGDDetailTabs(tabs.TabGroup):
    slug = "VNFFGD_details"
    tabs = (TemplateTab,)
    sticky = True
