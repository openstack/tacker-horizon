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

from horizon import exceptions
from horizon import forms
from horizon import tabs

from horizon.utils import memoized

from openstack_dashboard import api

from tacker_horizon.openstack_dashboard import api as tacker_api
from tacker_horizon.openstack_dashboard.dashboards.nfv.nscatalog \
    import tabs as nfv_tabs

from tacker_horizon.openstack_dashboard.dashboards.nfv.nscatalog \
    import forms as project_forms


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = nfv_tabs.NSCatalogTabs
    template_name = 'nfv/nscatalog/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class OnBoardNSView(forms.ModalFormView):
    form_class = project_forms.OnBoardNS
    template_name = 'nfv/nscatalog/onboardns.html'
    success_url = reverse_lazy("horizon:nfv:nscatalog:index")
    modal_id = "onboardns_modal"
    modal_header = _("OnBoard NS")
    submit_label = _("OnBoard NS")
    submit_url = "horizon:nfv:nscatalog:onboardns"

    @memoized.memoized_method
    def get_object(self):
        try:
            return api.nova.server_get(self.request,
                                       self.kwargs["instance_id"])
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to retrieve instance."))

    def get_initial(self):
        # return {"instance_id": self.kwargs["instance_id"]}
        return {}

    def get_context_data(self, **kwargs):
        context = super(OnBoardNSView, self).get_context_data(**kwargs)
        # instance_id = self.kwargs['instance_id']
        # context['instance_id'] = instance_id
        # context['instance'] = self.get_object()
        context['submit_url'] = reverse(self.submit_url)
        return context


class DetailView(tabs.TabView):
    tab_group_class = nfv_tabs.NSDDetailTabs
    template_name = 'nfv/nscatalog/detail.html'
    redirect_url = 'horizon:nfv:nscatalog:index'
    page_title = _("NSD Details: {{ nsd_id }}")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        nsd = self.get_data()
        context['nsd'] = nsd
        context['nsd_id'] = kwargs['nsd_id']
        context['url'] = reverse(self.redirect_url)
        return context

    @memoized.memoized_method
    def get_data(self):
        nsd_id = self.kwargs['nsd_id']

        try:
            template = None
            nsd = tacker_api.tacker.get_nsd(self.request, nsd_id)
            attributes_json = nsd['nsd']['attributes']
            template = attributes_json.get('nsd', None)
            nsd['template'] = template
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Unable to retrieve details for '
                                'NSD "%s".') % nsd_id,
                              redirect=redirect)
            raise exceptions.Http302(redirect)
        return nsd

    def get_tabs(self, request, *args, **kwargs):
        nsd = self.get_data()
        return self.tab_group_class(request, nsd=nsd, **kwargs)
