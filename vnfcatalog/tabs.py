from django.utils.translation import ugettext_lazy as _

import uuid

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.nfv.vnfcatalog import tables


class VNFCatalogItem(object):
    def __init__(self, name, description, services):
        self.id = uuid.uuid4()
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
            v1 = VNFCatalogItem("Vyatta vRouter", "Multi-service VNF", "NAT,Firewall,VPN")
            v2 = VNFCatalogItem("Palo Alto", "Firewall VNF", "Firewall")
            v3 = VNFCatalogItem("F5 Networks","Load Balancer","")

            instances = [v1, v2, v3]

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
