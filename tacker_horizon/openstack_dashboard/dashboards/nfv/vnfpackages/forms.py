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

import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from oslo_log import log as logging

from tacker_horizon.openstack_dashboard import api

LOG = logging.getLogger(__name__)


class UploadVnfPackage(forms.SelfHandlingForm):
    user_data = forms.JSONField(
        label=_("User Data"), required=False)
    source_type = forms.ChoiceField(
        label=_('VNF Package Source'),
        choices=[('url', _('URL')), ('file', _('File'))],
        widget=forms.Select(
            attrs={'class': 'switchable', 'data-slug': 'source'}))
    url = forms.URLField(
        widget=forms.TextInput(attrs={
            'class': 'switched',
            'data-switch-on': 'source',
            'data-source-url': _('URL')}),
        required=False)
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'switched',
            'data-switch-on': 'source',
            'data-source-url': _('User Name')}),
        required=False)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'switched',
            'data-switch-on': 'source',
            'data-source-url': _('Password')}),
        required=False)
    vnf_package = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'switched',
            'data-switch-on': 'source',
            'data-source-file': _('VNF Package')}),
        required=False)

    def __init__(self, request, *args, **kwargs):
        super(UploadVnfPackage, self).__init__(request, *args, **kwargs)

    def clean(self):
        data = super(UploadVnfPackage, self).clean()

        return data

    def handle(self, request, data):
        try:
            body = {}
            user_data = data.get('user_data', None)
            if user_data:
                body['userDefinedData'] = user_data
            response = api.tacker.create_vnf_package(request, body)
        except Exception:
            exceptions.handle(request,
                              _('Failed to create VNF Package.'))
            return False

        try:
            params = {}
            source_type = data.get('source_type', None)
            if source_type == 'url':
                params['url'] = data.get('url', None)
                user_name = data.get('user_name', None)
                password = data.get('password', None)
                if user_name:
                    params['userName'] = user_name
                    params['password'] = password
                api.tacker.upload_vnf_package(
                    request, response['id'], **params)
                messages.success(
                        request,
                        _('Accepted to upload VNF Package. '
                          '(id: %s)') % response['id'])
            else:
                file = request.FILES['vnf_package']
                if isinstance(file, TemporaryUploadedFile):
                    # Hack to fool Django, so we can keep file open.
                    file.file._closer.close_called = True
                elif isinstance(file, InMemoryUploadedFile):
                    # Clone a new file for InMemoryUploadedFile.
                    # Because the old one will be closed by Django.
                    file = SimpleUploadedFile(
                        file.name, file.read(), file.content_type)
                try:
                    api.tacker.upload_vnf_package(
                        request, response['id'], file, **params)
                    messages.success(
                        request,
                        _('Accepted to upload VNF Package. '
                          '(id: %s)') % response['id'])
                finally:
                    try:
                        filename = str(file.file.name)
                    except AttributeError:
                        pass
                    else:
                        try:
                            os.remove(filename)
                        except OSError as e:
                            LOG.warning(
                                'Failed to remove temporary file '
                                '%(file)s (%(e)s)',
                                {'file': filename, 'e': e})

        except Exception:
            exceptions.handle(request,
                              _('Failed to upload VNF Package. (id: %s)') %
                              response['id'])
            return False

        return True


class UpdateVnfPackage(forms.SelfHandlingForm):
    operationalState = forms.ChoiceField(
        label=_('Operational State'),
        required=False,
        choices=[(None, _(' ')),
                 ('ENABLED', _('ENABLED')),
                 ('DISABLED', _('DISABLED'))],
        widget=forms.Select(
            attrs={'class': 'switchable', 'data-slug': 'source'}))
    userData = forms.JSONField(label=_('User Data'),
                               required=False)

    def __init__(self, request, *args, **kwargs):
        super(UpdateVnfPackage, self).__init__(request, *args, **kwargs)

    def clean(self):
        data = super(UpdateVnfPackage, self).clean()
        operationalState = data.get('operationalState', None)
        userData = data.get('userData', None)
        if operationalState is None and userData is None:
            raise ValidationError(
                _("At least one of the \"operationalState\" or \
                  \"userDefinedData\" parameters shall be present."))
        return data

    def handle(self, request, data):
        try:
            vnfpkg_id = request.resolver_match.kwargs.get('id', None)
            body = {}
            operationalState = data.get('operationalState', None)
            if operationalState:
                body['operationalState'] = operationalState

            userDefinedData = data.get('userData', None)
            if userDefinedData:
                body['userDefinedData'] = userDefinedData
            api.tacker.update_vnf_package(request, vnfpkg_id, body)
            messages.success(request,
                             _('Update VNF Package. (id: %s)') % vnfpkg_id)

        except Exception:
            exceptions.handle(request,
                              _('Failed to update VNF Package. (id: %s)') %
                              vnfpkg_id)
            return False

        return True
