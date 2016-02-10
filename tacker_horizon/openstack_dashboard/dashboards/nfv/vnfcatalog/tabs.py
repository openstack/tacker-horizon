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


from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from tacker_horizon.openstack_dashboard import api
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfcatalog import tables


class VNFCatalogItem(object):
    def __init__(self, name, description, services, vnfd_id):
        self.id = vnfd_id
        self.name = name
        self.description = description
        self.services = services


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
            # marker = self.request.GET.get(
            #            tables.VNFCatalogTable._meta.pagination_param, None)

            self._has_more = False
            instances = []
            vnfds = api.tacker.vnfd_list(self.request)
            for vnfd in vnfds:
                services = vnfd['service_types']
                vnfd_services = []
                for s in services:
                    if s['service_type'] != 'vnfd':
                        vnfd_services.append(s['service_type'])
                vnfds_services_string = ""
                if len(vnfd_services) > 0:
                    vnfds_services_string = ', '.join(
                        [str(item) for item in vnfd_services])
                item = VNFCatalogItem(vnfd['name'],
                                      vnfd['description'],
                                      vnfds_services_string, vnfd['id'])
                instances.append(item)
            return instances
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
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


class VNFDDetailTabs(tabs.TabGroup):
    slug = "VNFD_details"
    tabs = (TemplateTab,)
    sticky = True
