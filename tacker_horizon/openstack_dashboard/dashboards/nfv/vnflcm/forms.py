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

import json
import time

from django.utils.translation import gettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from tacker_horizon.openstack_dashboard import api


class CreateVnfIdentifier(forms.SelfHandlingForm):
    vnfd_id = forms.CharField(label=_("VNFD ID"))
    param_file = forms.FileField(
       label=_("Param File"),
       widget=forms.FileInput(attrs={
            'class': 'switched',
            'data-switch-on': 'source',
            'data-source-upload': _('Param File')}),
       required=False)
    name = forms.CharField(label=_("Name"), required=False)
    description = forms.CharField(label=_("Description"), required=False)

    def __init__(self, request, *args, **kwargs):
        super(CreateVnfIdentifier, self).__init__(request, *args, **kwargs)

    def clean(self):
        data = super(CreateVnfIdentifier, self).clean()

        param_file = data.get('param_file', None)

        try:
            if param_file:
                metadata = self.files['param_file'].read()
                data['metadata'] = json.loads(metadata)
        except Exception as e:
            msg = _('Failed to read file: %s.') % e
            raise forms.ValidationError(msg)
        return data

    def handle(self, request, data):
        try:
            vnfd_id = data.get('vnfd_id', None)
            metadata = data.get('metadata', None)
            name = data.get('name', None)
            description = data.get('description', None)

            body = {}
            body['vnfdId'] = vnfd_id
            if metadata:
                body['metadata'] = metadata
            if name:
                body['vnfInstanceName'] = name
            if description:
                body['vnfInstanceDescription'] = description

            response = api.tacker.create_vnf_instance(request, body)
            messages.success(request,
                             _('Create VNF Identifier. (id: %s)') %
                             response['id'])

        except Exception:
            exceptions.handle(request, _('Failed to create VNF Identifier.'))
            return False

        return True


class InstantiateVnf(forms.SelfHandlingForm):
    param_file = forms.FileField(
       label=_("Param File"),
       widget=forms.FileInput(attrs={
            'class': 'switched',
            'data-switch-on': 'source',
            'data-source-upload': _('Param File')}))

    def __init__(self, request, *args, **kwargs):
        super(InstantiateVnf, self).__init__(request, *args, **kwargs)

    def clean(self):
        data = super(InstantiateVnf, self).clean()

        try:
            param_str = self.files['param_file'].read()
            param = json.loads(param_str)
            data['param_data'] = param
        except Exception as e:
            msg = _('Failed to read file: %s.') % e
            raise forms.ValidationError(msg)

        return data

    def handle(self, request, data):
        try:
            vnf_id = request.resolver_match.kwargs.get('id', None)
            param = data['param_data']
            api.tacker.instantiate_vnf_instance(request, vnf_id, param)
            messages.success(request,
                             _('Accepted to instantiate VNF Instance. '
                               '(id: %s)') % vnf_id)

        except Exception:
            exceptions.handle(request,
                              _('Failed to instantiate VNF Instance. '
                                '(id: %s)') % vnf_id)
            return False

        return True


class TerminateVnf(forms.SelfHandlingForm):
    termination_type = forms.ChoiceField(
        label=_('Termination Type'),
        required=True,
        choices=[('GRACEFUL', _('GRACEFUL')),
                 ('FORCEFUL', _('FORCEFUL'))],
        widget=forms.Select(
            attrs={'class': 'switchable', 'data-slug': 'source'}))
    termination_timeout = forms.IntegerField(
        min_value=0,
        required=False,
        label=_('Graceful Termination Timeout'))
    is_delete = forms.BooleanField(
        label=_('Delete VNF Instance'),
        required=False)

    def __init__(self, request, *args, **kwargs):
        super(TerminateVnf, self).__init__(request, *args, **kwargs)

    def clean(self):
        data = super(TerminateVnf, self).clean()
        return data

    def handle(self, request, data):
        try:
            is_delete = data.get('is_delete', False)
            vnf_id = request.resolver_match.kwargs.get('id', None)
            body = {}
            termination_type = data.get('termination_type', None)
            body['terminationType'] = termination_type
            termination_timeout = data.get('terminationTimeout', None)
            if termination_timeout:
                body['gracefulTerminationTimeout'] = termination_timeout
            api.tacker.terminate_vnf_instance(request, vnf_id, body)
            if not is_delete:
                messages.success(request,
                                 _('Accepted to terminate VNF Instance. '
                                   '(id: %s)') % vnf_id)
        except Exception:
            exceptions.handle(request,
                              _('Failed to terminate VNF Instance. '
                                '(id: %s)') % vnf_id)
            return False

        if is_delete:
            retry = 0
            retry_limit = 12
            while True:
                try:
                    time.sleep(10)
                    api.tacker.delete_vnf_instance(request, vnf_id)
                    messages.success(request,
                                     _('Delete VNF Identifier. (id: %s)') %
                                     vnf_id)
                    break
                except Exception as exc:
                    if 'is in progress' in str(exc):
                        # Conflict error occurs even if delete
                        # is executed immediately after terminate
                        retry = retry + 1
                        if retry >= retry_limit:
                            exceptions.handle(
                                request,
                                _('Delete VNF Identifier retry out. (id: %s)')
                                % vnf_id)
                            break
                        continue
                    else:
                        exceptions.handle(
                            request,
                            _('Failed to delete VNF Identifer. (id: %s)') %
                            vnf_id)
                        break
        return True


class HealVnf(forms.SelfHandlingForm):
    cause = forms.CharField(label=_("Cause"),
                            required=False)
    vnfc_instances = forms.CharField(
        label=_('VNFC Instance'), required=False, widget=forms.Textarea,
        help_text=_('Enter VNFC instance IDs in comma-separated list format.'))

    def __init__(self, request, *args, **kwargs):
        super(HealVnf, self).__init__(request, *args, **kwargs)

    def clean(self):
        data = super(HealVnf, self).clean()
        return data

    def handle(self, request, data):
        try:
            vnf_id = request.resolver_match.kwargs.get('id', None)
            body = {}
            cause = data.get('cause', None)
            if cause:
                body['cause'] = cause
            array_str = data.get('vnfc_instances', None)
            if array_str:
                array_str.replace('\n', '')
                vnfc_instance_ids = [s.strip() for s in array_str.split(',')]
                body['vnfcInstanceId'] = vnfc_instance_ids
            api.tacker.heal_vnf_instance(request, vnf_id, body)
            messages.success(request,
                             _('Accepted to heal VNF Instance. (id: %s)') %
                             vnf_id)

        except Exception:
            exceptions.handle(request,
                              _('Failed to heal VNF Instance. (id: %s)') %
                              vnf_id)
            return False

        return True


class UpdateVnf(forms.SelfHandlingForm):
    param_file = forms.FileField(
       label=_("Param File"),
       widget=forms.FileInput(attrs={
            'class': 'switched',
            'data-switch-on': 'source',
            'data-source-upload': _('Param File')}))

    def __init__(self, request, *args, **kwargs):
        super(UpdateVnf, self).__init__(request, *args, **kwargs)

    def clean(self):
        data = super(UpdateVnf, self).clean()
        try:
            param_str = self.files['param_file'].read()
            param = json.loads(param_str)
            data['param_data'] = param
        except Exception as e:
            msg = _('Failed to read file: %s.') % e
            raise forms.ValidationError(msg)

        return data

    def handle(self, request, data):
        try:
            vnf_id = request.resolver_match.kwargs.get('id', None)
            param = data['param_data']
            api.tacker.update_vnf_instance(request, vnf_id, param)
            messages.success(request,
                             _('Accepted to update VNF Instance. '
                               '(id: %s)') % vnf_id)

        except Exception:
            exceptions.handle(request,
                              _('Failed to update VNF Instance. '
                                '(id: %s)') % vnf_id)
            return False

        return True


class ScaleVnf(forms.SelfHandlingForm):
    scale_type = forms.ChoiceField(
        label=_('Type'),
        choices=[('SCALE_IN', _('SCALE_IN')),
                 ('SCALE_OUT', _('SCALE_OUT'))])
    aspect_id = forms.CharField(label=_("Aspect ID"))
    num_of_steps = forms.IntegerField(
        label=_("Number of Steps"), min_value=1, required=False)
    param_file = forms.FileField(
        label=_("Param File"),
        widget=forms.FileInput(attrs={
            'class': 'switched',
            'data-switch-on': 'source',
            'data-source-upload': _('Param File')}),
        required=False)

    def __init__(self, request, *args, **kwargs):
        super(ScaleVnf, self).__init__(request, *args, **kwargs)

    def clean(self):
        data = super(ScaleVnf, self).clean()

        param_file = data.get('param_file', None)

        try:
            if param_file:
                additional_params = self.files['param_file'].read()
                data['additional_params'] = json.loads(additional_params)
        except Exception as e:
            msg = _('Failed to read file: %s.') % e
            raise forms.ValidationError(msg)
        return data

    def handle(self, request, data):
        try:
            vnf_id = request.resolver_match.kwargs.get('id', None)
            scale_type = data.get('scale_type', None)
            aspect_id = data.get('aspect_id', None)
            num_of_steps = data.get('num_of_steps', None)
            additional_params = data.get('additional_params', None)

            body = {}
            body['type'] = scale_type
            body['aspectId'] = aspect_id
            if num_of_steps:
                body['numberOfSteps'] = num_of_steps
            if additional_params:
                body['additionalParams'] = additional_params

            api.tacker.scale_vnf_instance(request, vnf_id, body)
            messages.success(request,
                             _('Accepted to scale VNF Instance. '
                               '(id: %s)') % vnf_id)

        except Exception:
            exceptions.handle(request,
                              _('Failed to scale VNF Instance. '
                                '(id: %s)') % vnf_id)
            return False

        return True


class ChangeExternalVnfConnectivity(forms.SelfHandlingForm):
    param_file = forms.FileField(
       label=_("Param File"),
       widget=forms.FileInput(attrs={
            'class': 'switched',
            'data-switch-on': 'source',
            'data-source-upload': _('Param File')}))

    def __init__(self, request, *args, **kwargs):
        super(ChangeExternalVnfConnectivity,
              self).__init__(request, *args, **kwargs)

    def clean(self):
        data = super(ChangeExternalVnfConnectivity, self).clean()
        try:
            param_str = self.files['param_file'].read()
            param = json.loads(param_str)
            data['param_data'] = param
        except Exception as e:
            msg = _('Failed to read file: %s.') % e
            raise forms.ValidationError(msg)
        return data

    def handle(self, request, data):
        try:
            vnf_id = request.resolver_match.kwargs.get('id', None)
            param = data['param_data']
            api.tacker.change_ext_conn_vnf_instance(request, vnf_id, param)
            messages.success(request,
                             _('Accepted to change External VNF Connectivity. '
                               '(id: %s)') % vnf_id)

        except Exception:
            exceptions.handle(request,
                              _('Failed to change External VNF Connectivity. '
                                '(id: %s)') % vnf_id)
            return False

        return True


class ChangeCurrentVnfPackage(forms.SelfHandlingForm):
    param_file = forms.FileField(
       label=_("Param File"),
       widget=forms.FileInput(attrs={
            'class': 'switched',
            'data-switch-on': 'source',
            'data-source-upload': _('Param File')}))

    def __init__(self, request, *args, **kwargs):
        super(ChangeCurrentVnfPackage, self).__init__(request, *args, **kwargs)

    def clean(self):
        data = super(ChangeCurrentVnfPackage, self).clean()
        try:
            param_str = self.files['param_file'].read()
            param = json.loads(param_str)
            data['param_data'] = param
        except Exception as e:
            msg = _('Failed to read file: %s.') % e
            raise forms.ValidationError(msg)
        return data

    def handle(self, request, data):
        try:
            vnf_id = request.resolver_match.kwargs.get('id', None)
            param = data['param_data']
            api.tacker.change_vnfpkg_vnf_instance(request, vnf_id, param)
            messages.success(request,
                             _('Accepted to change Current VNF Package. '
                               '(id: %s)') % vnf_id)

        except Exception:
            exceptions.handle(request,
                              _('Failed to change Current VNF Package. '
                                '(id: %s)') % vnf_id)
            return False

        return True
