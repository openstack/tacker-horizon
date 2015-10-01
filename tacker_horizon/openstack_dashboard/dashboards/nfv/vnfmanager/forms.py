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
import yaml

from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from tacker_horizon.openstack_dashboard import api

LOG = logging.getLogger(__name__)

class AddService(forms.SelfHandlingForm):
    vnf_name = forms.CharField(max_length=80, label=_("VNF Name"))
    vnfd_id = forms.ChoiceField(label=_("VNF Catalog Name"))
    source_type = forms.ChoiceField(
        label=_('Parameter Value Source'),
        required=False,
        choices=[('file', _('File')),
                 ('raw', _('Direct Input'))],
        widget=forms.Select(
            attrs={'class': 'switchable', 'data-slug': 'source'}))

    param_file = forms.FileField(
        label=_("Parameter Value File"),
        help_text=_("A local Parameter value file to upload."),
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

    def __init__(self, request, *args, **kwargs):
        super(AddService, self).__init__(request, *args, **kwargs)

        try:
            vnfd_list = api.tacker.vnfd_list(request)
            available_choices = [(vnf['id'],vnf['name'])
                                 for vnf in vnfd_list]
        except Exception as e:
            msg = _('Failed to retrieve available VNF Catalog names: %s') % e
            LOG.error(msg)

        self.fields['vnfd_id'].choices = [('', _('Select a VNF Catalog Name'))
                                          ]+available_choices

    def clean(self):
        data = super(AddService, self).clean()

        param_file = data.get('param_file', None)
        param_raw = data.get('direct_input', None)

        if param_raw and param_file:
            raise ValidationError(
                _("Cannot specify both file and direct input."))

        if param_file and not param_file.name.endswith('.yaml'):
            raise ValidationError(
                _("Please upload .yaml file only."))

        if param_file:
            param_str = self.files['param_file'].read()
        else:
            param_str = data['direct_input']

        data['param_values'] = param_str

        return data

    def handle(self, request, data):
        try:
            vnf_name = data['vnf_name']
            vnfd_id = data['vnfd_id']
            vnf_arg = {'vnf': {'vnfd_id': vnfd_id, 'name':  vnf_name,
                               'attributes': {'param_values': data[
                                   'param_values']}}}
            api.tacker.create_vnf(request, vnf_arg)
            messages.success(request,
                             _('VNF %s create operation initiated.') % vnf_name)
            return True
        except Exception as e:
            exceptions.handle(request,
                              _(e.message))