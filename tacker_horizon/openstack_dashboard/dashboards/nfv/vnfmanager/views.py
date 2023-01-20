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

from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from oslo_log import log as logging
from oslo_serialization import jsonutils

from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon.utils import memoized

from tacker_horizon.openstack_dashboard import api as tacker_api
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfmanager \
    import forms as project_forms

from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfmanager \
    import tabs as nfv_tabs

LOG = logging.getLogger(__name__)


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = nfv_tabs.VNFManagerTabs
    template_name = 'nfv/vnfmanager/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class DeployVNFView(forms.ModalFormView):
    form_class = project_forms.DeployVNF
    template_name = 'nfv/vnfmanager/deploy_vnf.html'
    success_url = reverse_lazy("horizon:nfv:vnfmanager:index")
    modal_id = "deploy_vnf_modal"
    modal_header = _("Deploy VNF")
    submit_label = _("Deploy VNF")
    submit_url = "horizon:nfv:vnfmanager:deployvnf"

    # @memoized.memoized_method
    # def get_object(self):
    #    try:
    #        return api.nova.server_get(self.request,
    #                                   self.kwargs["instance_id"])
    #    except Exception:
    #        exceptions.handle(self.request,
    #                          _("Unable to retrieve instance."))

    def get_initial(self):
        # return {"instance_id": self.kwargs["instance_id"]}
        return {}

    def get_context_data(self, **kwargs):
        context = super(DeployVNFView, self).get_context_data(**kwargs)
        # instance_id = self.kwargs['instance_id']
        # context['instance_id'] = instance_id
        # context['instance'] = self.get_object()
        context['submit_url'] = reverse(self.submit_url)
        return context


class DetailView(tabs.TabView):
    tab_group_class = nfv_tabs.VNFDetailsTabs
    template_name = 'nfv/vnfmanager/detail.html'
    redirect_url = 'horizon:nfv:vnfmanager:index'
    page_title = _("VNF Details: {{ vnf_id }}")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        vnf = self.get_data()
        context['vnf'] = vnf
        context['vnf_id'] = kwargs['vnf_id']
        context['url'] = reverse(self.redirect_url)
        return context

    @memoized.memoized_method
    def get_data(self):
        vnf_id = self.kwargs['vnf_id']

        try:
            vnf = tacker_api.tacker.get_vnf(self.request, vnf_id)
            vnf["vnf"]["mgmt_ip_address"] = jsonutils.loads(
                    vnf["vnf"]["mgmt_ip_address"]) \
                if vnf["vnf"]["mgmt_ip_address"] else None
            return vnf
        except ValueError as e:
            msg = _('Cannot decode json : %s') % e
            LOG.error(msg)
        except KeyError as err:
            msg = _('Required field %s not specified') % err.args[0]
            LOG.error(msg)
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Unable to retrieve details for '
                                'VNF "%s".') % vnf_id,
                              redirect=redirect)
            raise exceptions.Http302(redirect)

    def get_tabs(self, request, *args, **kwargs):
        vnf = self.get_data()
        return self.tab_group_class(request, vnf=vnf, **kwargs)
