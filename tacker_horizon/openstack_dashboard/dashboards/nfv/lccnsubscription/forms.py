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

from django.utils.translation import gettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from tacker_horizon.openstack_dashboard import api


class CreateLccnSubscription(forms.SelfHandlingForm):
    param_file = forms.FileField(
       label=_("Param File"),
       widget=forms.FileInput(attrs={
            'class': 'switched',
            'data-switch-on': 'source',
            'data-source-upload': _('Param File')}))

    def __init__(self, request, *args, **kwargs):
        super(CreateLccnSubscription, self).__init__(request, *args, **kwargs)

    def clean(self):
        data = super(CreateLccnSubscription, self).clean()

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
            param = data['param_data']
            subsc = api.tacker.create_vnf_lcm_subscription(request, param)
            messages.success(
                request,
                _('Create LCCN Subscription. (id: %s)') % subsc['id'])

        except Exception:
            exceptions.handle(
                request,
                _('Failed to create LCCN Subscription.'))
            return False

        return True
