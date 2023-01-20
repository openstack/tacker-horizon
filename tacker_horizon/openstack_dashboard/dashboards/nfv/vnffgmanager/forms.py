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
from oslo_log import log as logging

from horizon import exceptions
from horizon import forms
from horizon import messages

from tacker_horizon.openstack_dashboard import api

LOG = logging.getLogger(__name__)


class DeployVNFFG(forms.SelfHandlingForm):
    vnffg_name = forms.CharField(max_length=255, label=_("VNFFG Name"))
    vnffgd_id = forms.ChoiceField(label=_("VNFFG Catalog Name"))
    vnf_mapping = forms.CharField(label=_("VNF Mapping"),
                                  required=False)
    symmetrical = forms.BooleanField(label=_("Symmetrical path"),
                                     required=False, help_text="Decides"
                                     " whether to automatically create a"
                                     " reverse patch for the NFP")

    def __init__(self, request, *args, **kwargs):
        super(DeployVNFFG, self).__init__(request, *args, **kwargs)

        try:
            vnffgd_list = api.tacker.vnffgd_list(request)
            available_choices_vnffgd = [(vnffg['id'], vnffg['name']) for
                                        vnffg in vnffgd_list]
        except Exception as e:
            available_choices_vnffgd = []
            msg = _('Failed to retrieve available VNFFG Catalog names: %s') % e
            LOG.error(msg)

        self.fields['vnffgd_id'].choices = [('', _('Select a VNFFG Catalog '
                                            'Name'))]+available_choices_vnffgd

    def clean(self):
        data = super(DeployVNFFG, self).clean()
        return data

    def list_vnfs(self, request):
        vnfs = [vnfs['name'] for vnfs in api.tacker.vnf_list(request)]
        return vnfs

    def handle(self, request, data):
        try:
            vnffg_name = data['vnffg_name']
            vnffgd_id = data['vnffgd_id']
            vnf_mapping = data['vnf_mapping']
            _vnf_mapping = dict()
            if vnf_mapping:
                _vnf_mappings = vnf_mapping.split(",")
                vnfs = self.list_vnfs(request)
                for mapping in _vnf_mappings:
                    vnfd_name, vnf = mapping.split(":", 1)
                    try:
                        if vnf in vnfs:
                            _vnf_mapping[vnfd_name] = vnf
                        else:
                            raise Exception
                    except Exception:
                        exceptions.handle(request, _('Specified VNF %s not'
                                                     ' found') % vnf)

            symmetrical = data['symmetrical']
            vnffg_arg = {'vnffg': {'vnffgd_id': vnffgd_id,
                                   'name': vnffg_name,
                                   'symmetrical': symmetrical,
                                   'vnf_mapping': _vnf_mapping}}

            api.tacker.create_vnffg(request, vnffg_arg)
            messages.success(request,
                             _('VNFFG %s create operation initiated.') %
                             vnffg_name)
            return True
        except Exception:
            exceptions.handle(request,
                              _('Failed to create VNFFG.'))
