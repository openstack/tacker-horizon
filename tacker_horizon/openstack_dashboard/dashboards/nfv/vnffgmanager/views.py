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
from django.utils.translation import ugettext_lazy as _
from oslo_log import log as logging
from oslo_serialization import jsonutils

from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon.utils import memoized

from tacker_horizon.openstack_dashboard import api as tacker_api
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnffgmanager \
    import forms as project_forms

from tacker_horizon.openstack_dashboard.dashboards.nfv.vnffgmanager \
    import tabs as nfv_tabs

LOG = logging.getLogger(__name__)


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = nfv_tabs.VNFFGManagerTabs
    template_name = 'nfv/vnffgmanager/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class DeployVNFFGView(forms.ModalFormView):
    form_class = project_forms.DeployVNFFG
    template_name = 'nfv/vnffgmanager/deploy_vnffg.html'
    success_url = reverse_lazy("horizon:nfv:vnffgmanager:index")
    modal_id = "deploy_vnffg_modal"
    modal_header = _("Deploy VNFFG")
    submit_label = _("Deploy VNFFG")
    submit_url = "horizon:nfv:vnffgmanager:deployvnffg"

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
        context = super(DeployVNFFGView, self).get_context_data(**kwargs)
        # instance_id = self.kwargs['instance_id']
        # context['instance_id'] = instance_id
        # context['instance'] = self.get_object()
        context['submit_url'] = reverse(self.submit_url)
        return context


class DetailView(tabs.TabView):
    tab_group_class = nfv_tabs.VNFFGDetailsTabs
    template_name = 'nfv/vnffgmanager/detail.html'
    redirect_url = 'horizon:nfv:vnffgmanager:index'
    page_title = _("VNFFG Details: {{ vnffg_id }}")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        vnffg = self.get_data()
        context['vnffg'] = vnffg
        context['vnffg_id'] = kwargs['vnffg_id']
        context['url'] = reverse(self.redirect_url)
        return context

    @memoized.memoized_method
    def get_data(self):
        vnffg_id = self.kwargs['vnffg_id']

        try:
            vnffg = tacker_api.tacker.get_vnffg(self.request, vnffg_id)
            vnffg["vnffg"]["mgmt_ip_address"] = jsonutils.loads(
                vnffg["vnffg"]["mgmt_ip_address"]) if vnffg["vnffg"].get(
                "mgmt_ip_address") else None
            return vnffg
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
                                'VNFFG "%s".') % vnffg_id,
                              redirect=redirect)
            raise exceptions.Http302(redirect)

    def get_tabs(self, request, *args, **kwargs):
        vnffg = self.get_data()
        return self.tab_group_class(request, vnffg=vnffg, **kwargs)
