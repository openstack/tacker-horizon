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

import logging

from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables

from horizon import exceptions
from horizon import forms
from horizon import messages

from tacker_horizon.openstack_dashboard import api

LOG = logging.getLogger(__name__)


class RegisterVim(forms.SelfHandlingForm):
    vim_name = forms.CharField(max_length=80, label=_("Name"))
    vim_description = forms.CharField(max_length=80, label=_("Description"),
                                      required=False)
    auth_url = forms.URLField(label=_("Auth URL"))
    username = forms.CharField(max_length=80, label=_("Username"))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(render_value=False))
    project_name = forms.CharField(max_length=80, label=_("Project Name"))

    def __init__(self, request, *args, **kwargs):
        super(RegisterVim, self).__init__(request, *args, **kwargs)

    def clean(self):
        data = super(RegisterVim, self).clean()
        return data

    @sensitive_variables('data', 'password')
    def handle(self, request, data):
        try:
            vim_name = data['vim_name']
            description = data['vim_description']
            password = data['password']
            username = data['username']
            project_name = data['project_name']
            auth_url = data['auth_url']
            vim_type = 'openstack'
            vim_arg = {'vim': {'name': vim_name, 'description': description,
                               'type': vim_type, 'auth_url': auth_url,
                               'auth_cred': {'username': username,
                                             'password': password},
                               'vim_project': {'name': project_name}}}
            api.tacker.create_vim(request, vim_arg)
            messages.success(request,
                             _('VIM %s create operation initiated.') %
                             vim_name)
            return True
        except Exception as e:
            exceptions.handle(request,
                              _('Failed to register VIM: %s') %
                              e.message)
