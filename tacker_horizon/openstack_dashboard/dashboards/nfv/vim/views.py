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


from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from horizon import tabs

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
