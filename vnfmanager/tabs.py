from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import tabs

from openstack_dashboard.dashboards.nfv.vnfmanager import tables
from openstack_dashboard import api
from openstack_dashboard.dashboards.nfv.vnfmanager.tables import VNFManagerItem
from openstack_dashboard.dashboards.nfv.vnfmanager.tables import VNFManagerItemList


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
            VNFManagerItemList.clear_list()
            vnfs = api.tacker.vnf_list(self.request)
            print "VNFs: " + str(vnfs)
            for vnf in vnfs:
                try:
                    vnf_services_str = vnf['attributes']['service_type']
                except KeyError:
                    vnf_services_str = ""
                try:
                    vnf_desc_str = vnf['description']
                except KeyError:
                    vnf_desc_str = ""
                obj = VNFManagerItem(vnf['name'],
                                     vnf_desc_str,
                                     vnf_services_str,
                                     'STATUS_UNUSED',
                                     vnf['status'],
                                     vnf['id'])
                VNFManagerItemList.add_item(obj)
            return VNFManagerItemList.VNFLIST_P
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []

class VNFManagerTabs(tabs.TabGroup):
    slug = "vnfmanager_tabs"
    tabs = (VNFManagerTab,)
    sticky = True
