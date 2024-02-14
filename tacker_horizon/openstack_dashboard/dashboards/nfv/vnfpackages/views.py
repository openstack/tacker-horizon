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


from django import http
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon.utils import memoized

from tacker_horizon.openstack_dashboard import api as tacker_api
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfpackages \
    import forms as project_forms
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnfpackages \
    import tabs as vnfpkg_tabs


def fetch_vnf_package(request, id):
    try:
        file = tacker_api.tacker.fetch_vnf_package(request, id)

    except Exception:
        exceptions.handle(request,
                          _('Failed to fetch VNF Package. (id: %s)') % id,
                          redirect="horizon:nfv:vnfpackages:index")
    response = http.HttpResponse(content_type='application/zip')
    response.write(file)
    response['Content-Disposition'] = (
        'attachment; filename="package-%s.zip"' % id)
    response['Content-Length'] = len(file)

    return response


class IndexView(tabs.TabbedTableView):
    tab_group_class = vnfpkg_tabs.VnfPackageTabs
    template_name = 'nfv/vnfpackages/index.html'


class UploadVnfPackageView(forms.ModalFormView):
    form_class = project_forms.UploadVnfPackage
    template_name = 'nfv/vnfpackages/upload_vnfpkg.html'
    success_url = reverse_lazy("horizon:nfv:vnfpackages:index")
    modal_id = "add_service_modal"
    modal_header = _("Upload VNF Package")
    submit_label = _("Upload VNF Package")
    submit_url = "horizon:nfv:vnfpackages:uploadvnfpkg"

    def get_context_data(self, **kwargs):
        context = super(UploadVnfPackageView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url)
        return context


class UpdateVnfPackageView(forms.ModalFormView):
    form_class = project_forms.UpdateVnfPackage
    template_name = 'nfv/vnfpackages/update_vnfpkg.html'
    success_url = reverse_lazy("horizon:nfv:vnfpackages:index")
    modal_id = "add_service_modal"
    modal_header = _("Update VNF Package Info")
    submit_label = _("Update VNF Package Info")
    submit_url = "horizon:nfv:vnfpackages:updatevnfpkg"

    def get_context_data(self, **kwargs):
        context = super(UpdateVnfPackageView, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        context['submit_url'] = reverse(self.submit_url,
                                        kwargs={'id': self.kwargs['id']})
        return context


class DetailView(tabs.TabView):
    tab_group_class = vnfpkg_tabs.VnfPackageDetailTabs
    template_name = 'nfv/vnfpackages/detail.html'
    redirect_url = 'horizon:nfv:vnfpackages:index'
    page_title = _("VNF Package Details: {{ id }}")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        vnfpkg = self.get_data()
        context['vnfpkg'] = vnfpkg
        context['id'] = kwargs['id']
        context['url'] = reverse(self.redirect_url)

        return context

    @memoized.memoized_method
    def get_data(self):
        vnfpkg_id = self.kwargs.get('id', None)

        try:
            vnfpkg = tacker_api.tacker.get_vnf_package(self.request, vnfpkg_id)
            vnfpkg['links'] = vnfpkg.get('_links', '')
            return vnfpkg
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(
                self.request,
                _('Failed to get VNF Package. (id: %s)') % vnfpkg_id,
                redirect=redirect)
            raise exceptions.Http302(redirect)

    def get_tabs(self, request, *args, **kwargs):
        vnfpkg = self.get_data()
        return self.tab_group_class(request, vnfpkg=vnfpkg, **kwargs)
