# Copyright (C) 2024 Fujitsu
# All Rights Reserved.
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
from django.utils.translation import gettext_lazy as _

from horizon import exceptions
from horizon import tabs
from horizon.utils import memoized

from tacker_horizon.openstack_dashboard import api as tacker_api
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnflcmopocc \
    import tabs as vnflcmopocc_tabs


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = vnflcmopocc_tabs.VnfLcmOpOccTabs
    template_name = 'nfv/vnflcmopocc/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class DetailView(tabs.TabView):
    tab_group_class = vnflcmopocc_tabs.VnfOpOccDetailTabs
    template_name = 'nfv/vnflcmopocc/detail.html'
    redirect_url = 'horizon:nfv:vnflcmopocc:index'
    page_title = _("LCM OP OCC Details: {{ id }}")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        vnflcmopocc = self.get_data()
        context['vnflcmopocc'] = vnflcmopocc
        context['id'] = kwargs['id']
        context['url'] = reverse(self.redirect_url)
        return context

    @memoized.memoized_method
    def get_data(self):
        opocc_id = self.kwargs['id']

        try:
            vnflcmopocc = tacker_api.tacker.get_vnf_lcm_op_occ(self.request,
                                                               opocc_id)
            vnflcmopocc['links'] = vnflcmopocc.get('_links', '')
            return vnflcmopocc
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(
                self.request,
                _('Failed to get VNF LCM operation occurrence. (id: %s)') %
                opocc_id,
                redirect=redirect)
            raise exceptions.Http302(redirect)

    def get_tabs(self, request, *args, **kwargs):
        vnflcmopocc = self.get_data()
        return self.tab_group_class(request, vnflcmopocc=vnflcmopocc, **kwargs)
