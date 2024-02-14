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
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfpmthreshold \
    import forms as project_forms
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfpmthreshold \
    import tabs as pmthreshold_tabs


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = pmthreshold_tabs.VnfPmThresholdTabs
    template_name = 'nfv/vnfpmthreshold/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class CreatePmThresholdView(forms.ModalFormView):
    form_class = project_forms.CreatePmThreshold
    template_name = 'nfv/vnfpmthreshold/create_pmthreshold.html'
    success_url = reverse_lazy("horizon:nfv:vnfpmthreshold:index")
    modal_id = "create_pmthreshold_modal"
    modal_header = _("Create PM Threshold")
    submit_label = _("Create PM Threshold")
    submit_url = "horizon:nfv:vnfpmthreshold:createpmthreshold"

    def get_context_data(self, **kwargs):
        context = super(CreatePmThresholdView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url)
        return context


class UpdatePmThresholdView(forms.ModalFormView):
    form_class = project_forms.UpdatePmThreshold
    template_name = 'nfv/vnfpmthreshold/update_pmthreshold.html'
    success_url = reverse_lazy("horizon:nfv:vnfpmthreshold:index")
    modal_id = "update_pmthreshold_modal"
    modal_header = _("Update PM Threshold")
    submit_label = _("Update PM Threshold")
    submit_url = "horizon:nfv:vnfpmthreshold:updatepmthreshold"

    def get_context_data(self, **kwargs):
        context = super(UpdatePmThresholdView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url,
                                        kwargs={'id': self.kwargs['id']})
        return context


class DetailView(tabs.TabView):
    tab_group_class = pmthreshold_tabs.VnfPmThresholdDetailTabs
    template_name = 'nfv/vnfpmthreshold/detail.html'
    redirect_url = 'horizon:nfv:vnfpmthreshold:index'
    page_title = _("PM Threshold Detail: {{ id }}")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        pmthreshold = self.get_data()
        context['pmthreshold'] = pmthreshold
        context['id'] = kwargs['id']
        context['url'] = reverse(self.redirect_url)
        return context

    @memoized.memoized_method
    def get_data(self):
        threshold_id = self.kwargs['id']

        try:
            pmthreshold = tacker_api.tacker.get_pm_threshold(self.request,
                                                             threshold_id)
            pmthreshold['links'] = pmthreshold.get('_links', '')
            pmthreshold['callback_uri'] = pmthreshold.get('callbackUri', '')
            pmthreshold['criteria'] = pmthreshold.get('criteria', '')
            pmthreshold['id'] = pmthreshold.get('id', '')
            pmthreshold['object_instance_id'] = pmthreshold.get(
                                                    'objectInstanceId', '')
            pmthreshold['object_type'] = pmthreshold.get('objectType', '')
            pmthreshold['sub_object_instance_ids'] = pmthreshold.get(
                                                'subObjectInstanceIds', '')
            return pmthreshold
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Failed to get PM Threshold. (id: %s)') %
                              threshold_id, redirect=redirect)
            raise exceptions.Http302(redirect)

    def get_tabs(self, request, *args, **kwargs):
        pmthreshold = self.get_data()
        return self.tab_group_class(request, pmthreshold=pmthreshold, **kwargs)
