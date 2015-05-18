from django.utils.translation import ugettext_lazy as _

import uuid

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.nfv.vnfcatalog import tables


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
            print "VNFD list API"
            vnfds = api.tacker.vnfd_list(self.request)
            print "VNFDs: " + str(vnfds)
            for vnfd in vnfds:
                print "VNFD entry " + str(vnfd)
                print "VNFD name " + vnfd['name']
                print "VNFD id " + vnfd['id']
                print "VNFD desc " + vnfd['description']
                services = vnfd['service_types']
                print "VNFD Services: " + str(services)
                vnfd_services =[]
                for s in services:
                    print "Serv:" + str(s)
                    if s['service_type'] != 'vnfd':
                        vnfd_services.append(s['service_type'])
                print "VNFDService: " + str(vnfd_services)
                vnfds_services_string = ""
                if len(vnfd_services) > 0:
                    vnfds_services_string = ', '.join([str(item) for item in vnfd_services])
                item = VNFCatalogItem(vnfd['name'], vnfd['description'], vnfds_services_string, vnfd['id'])
                instances.append(item)
            print "Instances: " + str(instances)
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
