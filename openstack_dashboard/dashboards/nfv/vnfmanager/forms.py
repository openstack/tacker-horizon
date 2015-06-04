from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard import api
from openstack_dashboard.dashboards.nfv.vnfmanager.tables import VNFManagerItem
from openstack_dashboard.dashboards.nfv.vnfmanager.tables import VNFManagerItemList


class AddService(forms.SelfHandlingForm):
    vnf_name = forms.CharField(max_length=80, label=_("VNF Name"))
    vnfd_id = forms.CharField(max_length=80, label=_("VNF Catalog ID"))

    def handle(self, request, data):
        try:
            vnf_name = data['vnf_name']
            vnfd_id = data['vnfd_id']
            print "VNF Name: " + vnf_name
            print "VNFD Id: " + vnfd_id
            vnf_arg = {'vnf': {'vnfd_id': vnfd_id, 'name':  vnf_name}}
            vnf_instance = api.tacker.create_vnf(request, vnf_arg)
            print "VNF Instance: " + str(vnf_instance)
            messages.success(request,
                             _('VNF %s has been created.') % vnf_name)
            return True
        except Exception:
            exceptions.handle(request,
                              _('Unable to create service.'))
