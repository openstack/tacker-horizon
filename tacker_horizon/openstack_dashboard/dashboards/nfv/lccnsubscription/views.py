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
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon.utils import memoized

from tacker_horizon.openstack_dashboard import api as tacker_api
from tacker_horizon.openstack_dashboard.dashboards.nfv.lccnsubscription \
    import forms as project_forms
from tacker_horizon.openstack_dashboard.dashboards.nfv.lccnsubscription \
    import tabs as lccnsubsctabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = lccnsubsctabs.LccnSubscriptionTabs
    template_name = 'nfv/lccnsubscription/index.html'


class CreateLccnSubscriptionView(forms.ModalFormView):
    form_class = project_forms.CreateLccnSubscription
    template_name = 'nfv/lccnsubscription/create_lccn_subscription.html'
    success_url = reverse_lazy("horizon:nfv:lccnsubscription:index")
    modal_id = "add_service_modal"
    modal_header = _("Create Lccn Subscription")
    submit_label = _("Create Lccn Subscription")
    submit_url = "horizon:nfv:lccnsubscription:createlccnsubscription"

    def get_context_data(self, **kwargs):
        context = super(
            CreateLccnSubscriptionView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url)
        return context


class DetailView(tabs.TabView):
    tab_group_class = lccnsubsctabs.LccnSubscDetailTabs
    template_name = 'nfv/lccnsubscription/detail.html'
    redirect_url = 'horizon:nfv:lccnsubscription:index'
    page_title = _("LCCN Subscription Detail")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        lccnsubscription = self.get_data()
        context['lccnsubscription'] = lccnsubscription
        context['id'] = kwargs['id']
        context['url'] = reverse(self.redirect_url)
        return context

    @memoized.memoized_method
    def get_data(self):
        subsc_id = self.kwargs.get('id', None)

        try:
            lccnsubscription = tacker_api.tacker.get_vnf_lcm_subscription(
                self.request, subsc_id)
            lccnsubscription['links'] = lccnsubscription.get('_links', '')
            return lccnsubscription
        except Exception as e:
            redirect = reverse(self.redirect_url)
            exceptions.handle(
                self.request,
                _('Failed to get LCCN Subscription. (id: %s)') % subsc_id,
                redirect=redirect)
            raise exceptions.Http302(redirect) from e

    def get_tabs(self, request, *args, **kwargs):
        lccnsubscription = self.get_data()
        return self.tab_group_class(
            request, lccnsubscription=lccnsubscription, **kwargs)
