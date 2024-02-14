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
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnffmsubscription \
    import forms as project_forms
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnffmsubscription \
    import tabs as subscription_tabs


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = subscription_tabs.VnfFmSubscriptionTabs
    template_name = 'nfv/vnffmsubscription/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class CreateVnfFmSubscriptionView(forms.ModalFormView):
    form_class = project_forms.CreateVnfFmSubscription
    template_name = 'nfv/vnffmsubscription/create_subscription.html'
    success_url = reverse_lazy("horizon:nfv:vnffmsubscription:index")
    modal_id = "create_subscription_modal"
    modal_header = _("Create Subscription")
    submit_label = _("Create Subscription")
    submit_url = "horizon:nfv:vnffmsubscription:createsubscription"

    def get_context_data(self, **kwargs):
        context = super(CreateVnfFmSubscriptionView,
                        self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url)
        return context


class DetailView(tabs.TabView):
    tab_group_class = subscription_tabs.VnfFmSubscriptionDetailTabs
    template_name = 'nfv/vnffmsubscription/detail.html'
    redirect_url = 'horizon:nfv:vnffmsubscription:index'
    page_title = _("Subscription Detail: {{ id }}")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        subscription = self.get_data()
        context['subscription'] = subscription
        context['id'] = kwargs['id']
        context['url'] = reverse(self.redirect_url)
        return context

    @memoized.memoized_method
    def get_data(self):
        subscription_id = self.kwargs['id']

        try:
            subscription = tacker_api.tacker.get_fm_subscription(
                self.request, subscription_id)
            subscription['links'] = subscription.get('_links', '')
            subscription['callback_uri'] = subscription.get('callbackUri', '')
            subscription['filter'] = subscription.get('filter', '')
            return subscription
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Failed to get FM Subscription. (id: %s)') %
                              subscription_id, redirect=redirect)
            raise exceptions.Http302(redirect)

    def get_tabs(self, request, *args, **kwargs):
        subscription = self.get_data()
        return self.tab_group_class(request,
                                    subscription=subscription, **kwargs)
