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

from django.utils.translation import gettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from tacker_horizon.openstack_dashboard import api


class UpdateVnfFmAlarm(forms.SelfHandlingForm):
    ack_state = forms.ChoiceField(
        label=_('ACK State'),
        choices=[('ACKNOWLEDGED', _('ACKNOWLEDGED')),
                 ('UNACKNOWLEDGED', _('UNACKNOWLEDGED'))])

    def __init__(self, request, *args, **kwargs):
        super(UpdateVnfFmAlarm, self).__init__(request, *args, **kwargs)

    def clean(self):
        data = super(UpdateVnfFmAlarm, self).clean()
        return data

    def handle(self, request, data):
        try:
            ack_state = data.get('ack_state', None)

            body = {}
            body['ackState'] = ack_state
            alarm_id = request.resolver_match.kwargs['id']
            api.tacker.update_fm_alarm(request, alarm_id, body)
            messages.success(request,
                             _('Update FM Alarm. (id: %s)') % alarm_id)
            return True
        except Exception:
            msg = _('Failed to update FM Alarm. (id: %s)') % alarm_id
            exceptions.handle(request, msg)
            return False
