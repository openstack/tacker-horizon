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

from horizon import tables


class UpdateVnfFmAlarm(tables.LinkAction):
    name = "updatealarm"
    verbose_name = _("Update Alarm")
    url = "horizon:nfv:vnffmalarm:updatealarm"
    classes = ("ajax-modal",)


class VnfFmAlarmTable(tables.DataTable):
    id = tables.Column('id', link="horizon:nfv:vnffmalarm:detail",
                       verbose_name=_("ID"))

    managed_object_id = tables.Column('managed_object_id',
                                      verbose_name=_("Managed Object ID"))
    ack_state = tables.Column('ack_state', verbose_name=_("Ack State"))
    event_type = tables.Column('event_type', verbose_name=_("Event Type"))
    perceived_severity = tables.Column('perceived_severity',
                                       verbose_name=_("Perceived Severity"))
    probable_cause = tables.Column('probable_cause',
                                   verbose_name=_("Probable Cause"))

    class Meta(object):
        name = "alarm"
        verbose_name = _("Alarm")
        pagination_param = 'vnffmalarm_marker'
        prev_pagination_param = 'prev_vnffmalarm_marker'
        table_actions = (tables.FilterAction,)
        row_actions = (UpdateVnfFmAlarm,)
