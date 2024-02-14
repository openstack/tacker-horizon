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
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnflcm \
    import forms as project_forms
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnflcm \
    import tabs as vnflcm_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = vnflcm_tabs.VnfLcmTabs
    template_name = 'nfv/vnflcm/index.html'


class CreateVnfIdentifierView(forms.ModalFormView):
    form_class = project_forms.CreateVnfIdentifier
    template_name = 'nfv/vnflcm/create_vnf_identifier.html'
    success_url = reverse_lazy("horizon:nfv:vnflcm:index")
    modal_id = "add_service_modal"
    modal_header = _("Create VNF Identifier")
    submit_label = _("Create VNF Identifier")
    submit_url = "horizon:nfv:vnflcm:createvnfidentifier"

    def get_context_data(self, **kwargs):
        context = super(
            CreateVnfIdentifierView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url)
        return context


class InstantiateVnfView(forms.ModalFormView):
    form_class = project_forms.InstantiateVnf
    template_name = 'nfv/vnflcm/instantiate_vnf.html'
    success_url = reverse_lazy("horizon:nfv:vnflcm:index")
    modal_id = "add_service_modal"
    modal_header = _("Instantiate VNF")
    submit_label = _("Instantiate VNF")
    submit_url = "horizon:nfv:vnflcm:instantiatevnf"

    def get_context_data(self, **kwargs):
        context = super(InstantiateVnfView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url,
                                        kwargs={'id': self.kwargs['id']})
        return context


class TerminateVnfView(forms.ModalFormView):
    form_class = project_forms.TerminateVnf
    template_name = 'nfv/vnflcm/terminate_vnf.html'
    success_url = reverse_lazy("horizon:nfv:vnflcm:index")
    modal_id = "add_service_modal"
    modal_header = _("Terminate VNF")
    submit_label = _("Terminate VNF")
    submit_url = "horizon:nfv:vnflcm:terminatevnf"

    def get_context_data(self, **kwargs):
        context = super(TerminateVnfView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url,
                                        kwargs={'id': self.kwargs['id']})
        return context


class HealVnfView(forms.ModalFormView):
    form_class = project_forms.HealVnf
    template_name = 'nfv/vnflcm/heal_vnf.html'
    success_url = reverse_lazy("horizon:nfv:vnflcm:index")
    modal_id = "add_service_modal"
    modal_header = _("Heal VNF")
    submit_label = _("Heal VNF")
    submit_url = "horizon:nfv:vnflcm:healvnf"

    def get_context_data(self, **kwargs):
        context = super(HealVnfView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url,
                                        kwargs={'id': self.kwargs['id']})
        return context


class UpdateVnfView(forms.ModalFormView):
    form_class = project_forms.UpdateVnf
    template_name = 'nfv/vnflcm/update_vnf.html'
    success_url = reverse_lazy("horizon:nfv:vnflcm:index")
    modal_id = "add_service_modal"
    modal_header = _("Update VNF")
    submit_label = _("Update VNF")
    submit_url = "horizon:nfv:vnflcm:updatevnf"

    def get_context_data(self, **kwargs):
        context = super(UpdateVnfView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url,
                                        kwargs={'id': self.kwargs['id']})
        return context


class ScaleVnfView(forms.ModalFormView):
    form_class = project_forms.ScaleVnf
    template_name = 'nfv/vnflcm/scale_vnf.html'
    success_url = reverse_lazy("horizon:nfv:vnflcm:index")
    modal_id = "add_service_modal"
    modal_header = _("Scale VNF")
    submit_label = _("Scale VNF")
    submit_url = "horizon:nfv:vnflcm:scalevnf"

    def get_context_data(self, **kwargs):
        context = super(ScaleVnfView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url,
                                        kwargs={'id': self.kwargs['id']})
        return context


class ChangeExternalVnfConnectivityView(forms.ModalFormView):
    form_class = project_forms.ChangeExternalVnfConnectivity
    template_name = 'nfv/vnflcm/change_connectivity.html'
    success_url = reverse_lazy("horizon:nfv:vnflcm:index")
    modal_id = "add_service_modal"
    modal_header = _("Change External VNF Connectivity")
    submit_label = _("Change External VNF Connectivity")
    submit_url = "horizon:nfv:vnflcm:changeconnectivity"

    def get_context_data(self, **kwargs):
        context = super(
            ChangeExternalVnfConnectivityView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url,
                                        kwargs={'id': self.kwargs['id']})
        return context


class ChangeCurrentVnfPackageView(forms.ModalFormView):
    form_class = project_forms.ChangeCurrentVnfPackage
    template_name = 'nfv/vnflcm/change_vnfpkg.html'
    success_url = reverse_lazy("horizon:nfv:vnflcm:index")
    modal_id = "add_service_modal"
    modal_header = _("Change Current VNF Package")
    submit_label = _("Change Current VNF Package")
    submit_url = "horizon:nfv:vnflcm:changevnfpkg"

    def get_context_data(self, **kwargs):
        context = super(
            ChangeCurrentVnfPackageView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url,
                                        kwargs={'id': self.kwargs['id']})
        return context


class DetailView(tabs.TabbedTableView):
    tab_group_class = vnflcm_tabs.VnfLcmDetailTabs
    template_name = 'nfv/vnflcm/detail.html'
    redirect_url = 'horizon:nfv:vnflcm:index'
    page_title = _("VNF Instance Detail: {{ id }}")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        vnflcm = self.get_data()
        context['vnflcm'] = vnflcm
        context['id'] = kwargs['id']
        context['url'] = reverse(self.redirect_url)
        return context

    @memoized.memoized_method
    def get_data(self):
        vnf_id = self.kwargs['id']

        try:
            vnflcm = tacker_api.tacker.get_vnf_instance(self.request, vnf_id)
            vnflcm['links'] = vnflcm.get('_links', '')
            return vnflcm
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(
                self.request,
                _('Failed to get VNF instance. (id: %s)') % vnf_id,
                redirect=redirect)
            raise exceptions.Http302(redirect)

    def get_tabs(self, request, *args, **kwargs):
        vnflcm = self.get_data()
        return self.tab_group_class(request, vnflcm=vnflcm, **kwargs)
