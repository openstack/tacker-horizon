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

from horizon import exceptions
from horizon import forms
from horizon import tabs

from horizon.utils import memoized

from openstack_dashboard import api

from tacker_horizon.openstack_dashboard import api as tacker_api
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfcatalog \
    import tabs as nfv_tabs

from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfcatalog \
    import forms as project_forms


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = nfv_tabs.VNFCatalogTabs
    template_name = 'nfv/vnfcatalog/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class OnBoardVNFView(forms.ModalFormView):
    form_class = project_forms.OnBoardVNF
    template_name = 'nfv/vnfcatalog/onboardvnf.html'
    success_url = reverse_lazy("horizon:nfv:vnfcatalog:index")
    modal_id = "onboardvnf_modal"
    modal_header = _("OnBoard VNF")
    submit_label = _("OnBoard VNF")
    submit_url = "horizon:nfv:vnfcatalog:onboardvnf"

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
        context = super(OnBoardVNFView, self).get_context_data(**kwargs)
        # instance_id = self.kwargs['instance_id']
        # context['instance_id'] = instance_id
        # context['instance'] = self.get_object()
        context['submit_url'] = reverse(self.submit_url)
        return context


class DetailView(tabs.TabView):
    tab_group_class = nfv_tabs.VNFDDetailTabs
    template_name = 'nfv/vnfcatalog/detail.html'
    redirect_url = 'horizon:nfv:vnfcatalog:index'
    page_title = _("VNFD Details: {{ vnfd_id }}")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        vnfd = self.get_data()
        context['vnfd'] = vnfd
        context['vnfd_id'] = kwargs['vnfd_id']
        context['url'] = reverse(self.redirect_url)
        return context

    @memoized.memoized_method
    def get_data(self):
        vnfd_id = self.kwargs['vnfd_id']

        try:
            template = None
            vnfd = tacker_api.tacker.get_vnfd(self.request, vnfd_id)
            attributes_json = vnfd['vnfd']['attributes']
            template = attributes_json.get('vnfd', None)
            vnfd['template'] = template
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Unable to retrieve details for '
                                'VNFD "%s".') % vnfd_id,
                              redirect=redirect)
            raise exceptions.Http302(redirect)
        return vnfd

    def get_tabs(self, request, *args, **kwargs):
        vnfd = self.get_data()
        return self.tab_group_class(request, vnfd=vnfd, **kwargs)
