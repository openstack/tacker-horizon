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

from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon.utils import memoized

from tacker_horizon.openstack_dashboard import api as tacker_api
from tacker_horizon.openstack_dashboard.dashboards.nfv.nsmanager \
    import forms as project_forms

from tacker_horizon.openstack_dashboard.dashboards.nfv.nsmanager \
    import tabs as nfv_tabs

LOG = logging.getLogger(__name__)


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = nfv_tabs.NSManagerTabs
    template_name = 'nfv/nsmanager/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class DeployNSView(forms.ModalFormView):
    form_class = project_forms.DeployNS
    template_name = 'nfv/nsmanager/deploy_ns.html'
    success_url = reverse_lazy("horizon:nfv:nsmanager:index")
    modal_id = "deploy_ns_modal"
    modal_header = _("Deploy NS")
    submit_label = _("Deploy NS")
    submit_url = "horizon:nfv:nsmanager:deployns"

    def get_initial(self):
        # return {"instance_id": self.kwargs["instance_id"]}
        return {}

    def get_context_data(self, **kwargs):
        context = super(DeployNSView, self).get_context_data(**kwargs)
        # instance_id = self.kwargs['instance_id']
        # context['instance_id'] = instance_id
        # context['instance'] = self.get_object()
        context['submit_url'] = reverse(self.submit_url)
        return context


class DetailView(tabs.TabView):
    tab_group_class = nfv_tabs.NSDetailsTabs
    template_name = 'nfv/nsmanager/detail.html'
    redirect_url = 'horizon:nfv:nsmanager:index'
    page_title = _("NS Details: {{ ns_id }}")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        ns = self.get_data()
        context['ns'] = ns
        context['ns_id'] = kwargs['ns_id']
        context['url'] = reverse(self.redirect_url)
        return context

    @memoized.memoized_method
    def get_data(self):
        ns_id = self.kwargs['ns_id']

        try:
            ns = tacker_api.tacker.get_ns(self.request, ns_id)
            return ns
        except ValueError as e:
            msg = _('Cannot decode json : %s') % e
            LOG.error(msg)
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Unable to retrieve details for '
                                'NS "%s".') % ns_id,
                              redirect=redirect)
            raise exceptions.Http302(redirect)

    def get_tabs(self, request, *args, **kwargs):
        ns = self.get_data()
        return self.tab_group_class(request, ns=ns, **kwargs)
