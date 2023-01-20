# Copyright 2016 Brocade Communications System, Inc.
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
from tacker_horizon.openstack_dashboard.dashboards.nfv.vim \
    import forms as project_forms

from tacker_horizon.openstack_dashboard.dashboards.nfv.vim \
    import tabs as vim_tabs


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = vim_tabs.VIMTabs
    template_name = 'nfv/vim/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class RegisterVIMView(forms.ModalFormView):
    form_class = project_forms.RegisterVim
    template_name = 'nfv/vim/registervim.html'
    success_url = reverse_lazy("horizon:nfv:vim:index")
    modal_id = "add_service_modal"
    modal_header = _("Register VIM")
    submit_label = _("Register VIM")
    submit_url = "horizon:nfv:vim:registervim"

    def get_context_data(self, **kwargs):
        context = super(RegisterVIMView, self).get_context_data(**kwargs)
        context['submit_url'] = reverse(self.submit_url)
        return context


class DetailView(tabs.TabView):
    tab_group_class = vim_tabs.VIMDetailsTabs
    template_name = 'nfv/vim/detail.html'
    redirect_url = 'horizon:nfv:vim:index'
    page_title = _("VIM Event Details: {{ vim_id }}")

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        vim = self.get_data()
        context['vim'] = vim
        context['vim_id'] = kwargs['vim_id']
        context['url'] = reverse(self.redirect_url)
        return context

    @memoized.memoized_method
    def get_data(self):
        vim_id = self.kwargs['vim_id']

        try:
            vim = tacker_api.tacker.get_vim(self.request, vim_id)
            return vim
        except Exception:
            redirect = reverse(self.redirect_url)
            exceptions.handle(self.request,
                              _('Unable to retrieve details for '
                                'VIM "%s".') % vim_id,
                              redirect=redirect)
            raise exceptions.Http302(redirect)

    def get_tabs(self, request, *args, **kwargs):
        vim = self.get_data()
        return self.tab_group_class(request, vim=vim, **kwargs)
