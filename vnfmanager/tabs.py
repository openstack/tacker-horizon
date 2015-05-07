from django.utils.translation import ugettext_lazy as _
import uuid
from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.nfv.vnfmanager import tables


class VNFManagerItem(object):
    def __init__(self, name, description, vnfs, status):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
        self.vnfs = vnfs
        self.status = status


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
            #marker = self.request.GET.get(
            #            tables.VNFManagerTable._meta.pagination_param, None)

            #instances, self._has_more = api.nova.server_list(
            #    self.request,
            #    search_opts={'marker': marker, 'paginate': True})
            self._has_more = True
            v1 = VNFManagerItem("node-SJ-Site-1", "ACME SJ-CA-site-1", "VNF1, VNF2, VNF2", "Active")
            v2 = VNFManagerItem("node-SJ-Site-2", "ACME SJ-CA-site-2", "VNF1, VNF2", "Active")
            instances = [v1,v2]
            return instances
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []

class VNFManagerTabs(tabs.TabGroup):
    slug = "vnfmanager_tabs"
    tabs = (VNFManagerTab,)
    sticky = True
