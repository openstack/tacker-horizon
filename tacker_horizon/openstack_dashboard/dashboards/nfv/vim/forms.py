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

from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_variables

from horizon import exceptions
from horizon import forms
from horizon import messages

from tacker_horizon.openstack_dashboard import api


class RegisterVim(forms.SelfHandlingForm):
    vim_type = forms.ChoiceField(choices=api.tacker.SUPPORTED_VIM_TYPES,
                                 label=_("VIM Type"))
    vim_name = forms.CharField(max_length=255, label=_("Name"))
    vim_description = forms.CharField(widget=forms.widgets.Textarea(
                                      attrs={'rows': 4}),
                                      label=_("Description"),
                                      required=False)
    auth_url = forms.URLField(label=_("Auth URL"))
    auth_method = forms.ChoiceField(widget=forms.widgets.RadioSelect,
                                    choices=api.tacker.AUTH_METHODS,
                                    initial="basic",
                                    label=_("Auth Method"))
    username = forms.CharField(max_length=80,
                               initial="admin",
                               label=_("Username"))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(render_value=False))
    cert_verify = forms.ChoiceField(widget=forms.widgets.RadioSelect,
                                    choices=api.tacker.CERT_VERIFY_TYPES,
                                    initial="True",
                                    label=_("Cert Verify"))
    bearer_token = forms.CharField(widget=forms.widgets.Textarea(
                                   attrs={'rows': 4}),
                                   label=_("Bearer Token"))
    project_name = forms.CharField(max_length=80, label=_("Project Name"))
    domain_name = forms.CharField(max_length=80, label=_("Domain Name"),
                                  help_text=_('Applicable for OpenStack site '
                                              'running keystone v3. Run '
                                              'openstack domain list from '
                                              'CLI to find domain name'),
                                  required=False)
    ssl_ca_cert = forms.CharField(widget=forms.widgets.Textarea(
                                  attrs={'rows': 4}),
                                  label=_("SSL CA Certificate"),
                                  required=False)
    is_default = forms.BooleanField(
        label=_("Default"),
        initial=False,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'switched',
            }
        )
    )

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
            is_default = data['is_default']
            auth_url = data['auth_url']
            domain_name = data['domain_name']
            cert_verify = data.get('cert_verify', api.tacker.CERT_TRUE_TYPE)
            if cert_verify not in [api.tacker.CERT_TRUE_TYPE,
                                   api.tacker.CERT_FALSE_TYPE]:
                raise forms.ValidationError("cert_verify type not supported.")
            auth_cred = {'username': username,
                         'password': password,
                         'user_domain_name': domain_name,
                         'cert_verify': cert_verify}
            bearer_token = data['bearer_token'].replace('None', '')
            ssl_ca_cert = data['ssl_ca_cert'].replace('\r\n', ' ')
            vim_type = data['vim_type']
            if vim_type == 'kubernetes':
                auth_cred = {'username': username,
                             'password': password}
                # if bearer_token is provided, use it instead
                if bearer_token:
                    auth_cred = {'bearer_token': bearer_token}
                # only k8s vim needs ssl_ca_cert and it's optional
                if ssl_ca_cert:
                    auth_cred['ssl_ca_cert'] = ssl_ca_cert
            vim_arg = {'vim': {'name': vim_name, 'description': description,
                               'type': vim_type, 'auth_url': auth_url,
                               'auth_cred': auth_cred,
                               'vim_project': {'name': project_name,
                                               'project_domain_name':
                                                   domain_name},
                               'is_default': is_default}}
            api.tacker.create_vim(request, vim_arg)
            messages.success(request,
                             _('VIM %s create operation initiated.') %
                             vim_name)
            return True
        except Exception:
            exceptions.handle(request,
                              _('Failed to register VIM.'))
