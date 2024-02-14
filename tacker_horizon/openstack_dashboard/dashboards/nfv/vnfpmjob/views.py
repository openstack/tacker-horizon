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
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfpmjob \
    import forms as project_forms
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfpmjob \
    import tabs as pmjob_tabs


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = pmjob_tabs.VnfPmJobTabs
    template_name = 'nfv/vnfpmjob/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class CreatePmJobView(forms.ModalFormView):
    form_class = project_forms.CreatePmJob
    template_name = 'nfv/vnfpmjob/create_pmjob.html'
    success_url = reverse_lazy("horizon:nfv:vnfpmjob:index")
    modal_id = "create_pmjob_modal"
    modal_header = _("Create PM Job")
    submit_label = _("Create PM Job")
    submit_url = "horizon:nfv:vnfpmjob:createpmjob"

    def get_context_data(self, **kwargs):
        context = super(CreatePmJobView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url)
        return context


class UpdatePmJobView(forms.ModalFormView):
    form_class = project_forms.UpdatePmJob
    template_name = 'nfv/vnfpmjob/update_pmjob.html'
    success_url = reverse_lazy("horizon:nfv:vnfpmjob:index")
    modal_id = "update_pmjob_modal"
    modal_header = _("Update PM Job")
    submit_label = _("Update PM Job")
    submit_url = "horizon:nfv:vnfpmjob:updatepmjob"

    def get_context_data(self, **kwargs):
        context = super(UpdatePmJobView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url,
                                        kwargs={'id': self.kwargs['id']})
        return context


class DetailView(tabs.TabView):
    tab_group_class = pmjob_tabs.VnfPmJobDetailTabs
    template_name = 'nfv/vnfpmjob/detail.html'
    redirect_url = 'horizon:nfv:vnfpmjob:index'
    page_title = _("PM Job Detail: {{ id }}")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        pmjob = self.get_data()
        context['pmjob'] = pmjob
        context['id'] = kwargs['id']
        context['url'] = reverse(self.redirect_url)
        return context

    @memoized.memoized_method
    def get_data(self):
        job_id = self.kwargs['id']

        try:
            pmjob = tacker_api.tacker.get_pm_job(self.request, job_id)
            pmjob['links'] = pmjob.get('_links', '')
            pmjob['callback_uri'] = pmjob.get('callbackUri', '')
            pmjob['criteria'] = pmjob.get('criteria', '')
            pmjob['id'] = pmjob.get('id', '')
            pmjob['object_instance_ids'] = pmjob.get('objectInstanceIds', '')
            pmjob['object_type'] = pmjob.get('objectType', '')
            pmjob['sub_object_instance_ids'] = pmjob.get(
                                                'subObjectInstanceIds', '')
            pmjob['reports'] = self.add_reportid(pmjob.get('reports', ''))

            return pmjob
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Failed to get PM Job. (id: %s)') %
                              job_id, redirect=redirect)
            raise exceptions.Http302(redirect)

    def get_tabs(self, request, *args, **kwargs):
        pmjob = self.get_data()
        return self.tab_group_class(request, pmjob=pmjob, **kwargs)

    def add_reportid(self, reports=None):
        repots_new = []
        for report in reports:
            href = report.get('href', '')
            target_reports = 'reports/'
            target_jobs = 'pm_jobs/'
            idx_reports = href.find(target_reports)
            idx_jobs = href.find(target_jobs)

            if (0 <= idx_reports) and (0 <= idx_jobs):
                report['reportId'] = href[idx_reports+len(target_reports):]
                report['id'] = href[idx_jobs+len(target_jobs):idx_reports-1]

            repots_new.extend([report])
        return repots_new


class ReportDetailView(tabs.TabView):
    tab_group_class = pmjob_tabs.VnfPmJobReportDetailTabs
    template_name = 'nfv/vnfpmjob/detail.html'
    redirect_url = 'horizon:nfv:vnfpmjob:index'
    page_title = _("PM Job Report: {{ reportId }}")
    href_url = 'horizon:nfv:vnfpmjob:reportdetail'

    def get_context_data(self, **kwargs):
        context = super(ReportDetailView, self).get_context_data(**kwargs)
        report = self.get_data()
        context['report'] = report
        context['id'] = kwargs['id']
        context['reportId'] = kwargs['reportId']
        context['url'] = reverse(self.redirect_url)
        context['submit_url'] = reverse(
                self.href_url, kwargs={'id': self.kwargs['id'],
                                       'reportId': self.kwargs['reportId']})
        return context

    @memoized.memoized_method
    def get_data(self):

        job_id = self.kwargs['id']
        report_id = self.kwargs['reportId']

        try:
            report = tacker_api.tacker.get_pm_report(self.request,
                                                     job_id, report_id)
            report['entries'] = report.get('entries', '')
            return report
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Failed to get Report. (id: %s)') % report_id,
                              redirect=redirect)
            raise exceptions.Http302(redirect)

    def get_tabs(self, request, *args, **kwargs):
        report = self.get_data()
        return self.tab_group_class(request, report=report, **kwargs)
