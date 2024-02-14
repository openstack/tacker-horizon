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
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnffmalarm \
    import forms as project_forms
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnffmalarm \
    import tabs as alarm_tabs


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = alarm_tabs.VnfFmAlarmTabs
    template_name = 'nfv/vnffmalarm/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class UpdateVnfFmAlarmView(forms.ModalFormView):
    form_class = project_forms.UpdateVnfFmAlarm
    template_name = 'nfv/vnffmalarm/update_alarm.html'
    success_url = reverse_lazy("horizon:nfv:vnffmalarm:index")
    modal_id = "update_alarm_modal"
    modal_header = _("Update Alarm")
    submit_label = _("Update Alarm")
    submit_url = "horizon:nfv:vnffmalarm:updatealarm"

    def get_context_data(self, **kwargs):
        context = super(UpdateVnfFmAlarmView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url,
                                        kwargs={'id': self.kwargs['id']})
        return context


class DetailView(tabs.TabView):
    tab_group_class = alarm_tabs.VnfFmAlarmDetailTabs
    template_name = 'nfv/vnffmalarm/detail.html'
    redirect_url = 'horizon:nfv:vnffmalarm:index'
    page_title = _("Alarm Detail: {{ id }}")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        alarm = self.get_data()
        context['alarm'] = alarm
        context['id'] = kwargs['id']
        context['url'] = reverse(self.redirect_url)
        return context

    @memoized.memoized_method
    def get_data(self):
        alarm_id = self.kwargs['id']

        try:
            alarm = tacker_api.tacker.get_fm_alarm(self.request, alarm_id)
            alarm['links'] = alarm.get('_links', '')
            return alarm
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Failed to get FM Alarm. (id: %s)') % alarm_id,
                              redirect=redirect)
            raise exceptions.Http302(redirect)

    def get_tabs(self, request, *args, **kwargs):
        alarm = self.get_data()
        return self.tab_group_class(request, alarm=alarm, **kwargs)
