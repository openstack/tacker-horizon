# Copyright 2015 Brocade Communications System, Inc.
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

from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from tacker_horizon.openstack_dashboard import api

LOG = logging.getLogger(__name__)


class DeployVNF(forms.SelfHandlingForm):
    vnf_name = forms.CharField(max_length=80, label=_("VNF Name"),
                               required=False)
    vnfd_id = forms.ChoiceField(label=_("VNF Catalog Name"))
    vim_id = forms.ChoiceField(label=_("VIM Name"), required=False)
    region_name = forms.CharField(label=_("Region Name"), required=False)
    source_type = forms.ChoiceField(
        label=_('Parameter Value Source'),
        required=False,
        choices=[('file', _('File')),
                 ('raw', _('Direct Input'))],
        widget=forms.Select(
            attrs={'class': 'switchable', 'data-slug': 'source'}))

    param_file = forms.FileField(
        label=_('Parameter Value File'),
        help_text=_('A local Parameter Value file to upload.'),
        widget=forms.FileInput(
            attrs={'class': 'switched', 'data-switch-on': 'source',
                   'data-source-file': _('Parameter Value File')}),
        required=False)

    direct_input = forms.CharField(
        label=_('Parameter Value YAML'),
        help_text=_('The YAML formatted contents of Parameter Values.'),
        widget=forms.widgets.Textarea(
            attrs={'class': 'switched', 'data-switch-on': 'source',
                   'data-source-raw': _('Parameter Values')}),
        required=False)

    config_type = forms.ChoiceField(
        label=_('Configuration Value Source'),
        required=False,
        choices=[('file', _('File')),
                 ('raw', _('Direct Input'))],
        widget=forms.Select(
            attrs={'class': 'switchable', 'data-slug': 'config'}))

    config_file = forms.FileField(
        label=_('Configuration Value File'),
        help_text=_('VNF Configuration file with YAML '
                    'formatted contents to upload.'),
        widget=forms.FileInput(
            attrs={'class': 'switched', 'data-switch-on': 'config',
                   'data-config-file': _('Configuration Value File')}),
        required=False)

    config_input = forms.CharField(
        label=_('Configuration Value YAML'),
        help_text=_('YAML formatted VNF configuration text.'),
        widget=forms.widgets.Textarea(
            attrs={'class': 'switched', 'data-switch-on': 'config',
                   'data-config-raw': _('Configuration Values')}),
        required=False)

    def __init__(self, request, *args, **kwargs):
        super(DeployVNF, self).__init__(request, *args, **kwargs)

        try:
            vnfd_list = api.tacker.vnfd_list(request)
            available_choices_vnfd = [(vnf['id'], vnf['name']) for vnf in
                                      vnfd_list]
        except Exception as e:
            available_choices_vnfd = []
            msg = _('Failed to retrieve available VNF Catalog names: %s') % e
            LOG.error(msg)

        try:
            vim_list = api.tacker.vim_list(request)
            available_choices_vims = [(vim['id'], vim['name']) for vim in
                                      vim_list]

        except Exception as e:
            available_choices_vims = []
            msg = _('Failed to retrieve available VIM names: %s') % e
            LOG.error(msg)

        self.fields['vnfd_id'].choices = [('', _('Select a VNF Catalog Name'))
                                          ]+available_choices_vnfd
        self.fields['vim_id'].choices = [('',
                                          _('Select a VIM Name'))
                                         ]+available_choices_vims

    def clean(self):
        data = super(DeployVNF, self).clean()

        param_file = data.get('param_file', None)
        param_raw = data.get('direct_input', None)

        if param_raw and param_file:
            raise ValidationError(
                _("Cannot specify both file and direct input."))

        if param_file and not param_file.name.endswith('.yaml'):
            raise ValidationError(
                _("Please upload .yaml file only."))

        if param_file:
            data['param_values'] = self.files['param_file'].read()
        elif param_raw:
            data['param_values'] = data['direct_input']
        else:
            data['param_values'] = None

        config_file = data.get('config_file', None)
        config_raw = data.get('config_input', None)

        if config_file and config_raw:
            raise ValidationError(
                _("Cannot specify both file and direct input."))

        if config_file and not config_file.name.endswith('.yaml'):
            raise ValidationError(_("Only .yaml file uploads supported"))

        if config_file:
            data['config_values'] = self.files['config_file'].read()
        elif config_raw:
            data['config_values'] = data['config_input']
        else:
            data['config_values'] = None

        return data

    def handle(self, request, data):
        try:
            vnf_name = data['vnf_name']
            vnfd_id = data['vnfd_id']
            vim_id = data['vim_id']
            region_name = data['region_name']
            param_val = data['param_values']
            config_val = data['config_values']
            vnf_arg = {'vnf': {'vnfd_id': vnfd_id, 'name':  vnf_name,
                               'vim_id': vim_id}}
            if region_name:
                vnf_arg.setdefault('placement_attr', {})[
                    region_name] = region_name
            vnf_attr = vnf_arg['vnf'].setdefault('attributes', {})
            if param_val:
                vnf_attr['param_values'] = param_val
            if config_val:
                vnf_attr['config'] = config_val

            api.tacker.create_vnf(request, vnf_arg)
            messages.success(request,
                             _('VNF %s create operation initiated.') %
                             vnf_name)
            return True
        except Exception as e:
            exceptions.handle(request,
                              _('Failed to create VNF: %s') %
                              e.message)
