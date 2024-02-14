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
from horizon import tabs
from horizon import utils as horizon_utils

from tacker_horizon.openstack_dashboard import api
from tacker_horizon.openstack_dashboard.dashboards.nfv.vnffmalarm \
    import tables


class VnfFmAlarmItem(object):
    def __init__(self, alarm_id, managed_object_id, ack_state, event_type,
                 perceived_severity, probable_cause):
        self.id = alarm_id
        self.name = alarm_id
        self.managed_object_id = managed_object_id
        self.ack_state = ack_state
        self.event_type = event_type
        self.perceived_severity = perceived_severity
        self.probable_cause = probable_cause


class VnfFmAlarmTab(tabs.TableTab):
    name = _("VNFFMAlarm Tab")
    slug = "vnffmalarm_tab"
    table_classes = (tables.VnfFmAlarmTable,)
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def has_prev_data(self, table):
        return self._has_prev

    def has_more_data(self, table):
        return self._has_more

    def get_alarm_data(self):
        try:
            self._has_prev = False
            page_size = horizon_utils.functions.get_page_size(self.request)
            marker = self.request.GET.get("vnffmalarm_marker", None)
            prev_marker = self.request.GET.get("prev_vnffmalarm_marker", None)
            alarms = api.tacker.list_fm_alarms(self.request)

            if marker is not None or prev_marker is not None:
                for i, alarm in enumerate(alarms):
                    if alarm["id"] == marker and i < len(alarms) - 1:
                        alarms = alarms[i + 1:]
                        self._has_prev = True
                        break
                    if alarm["id"] == prev_marker and i > page_size:
                        alarms = alarms[i - page_size:]
                        self._has_prev = True
                        break

            if len(alarms) > page_size:
                self._has_more = True
            else:
                self._has_more = False

            rows = []
            for i, alarm in enumerate(alarms):
                if i >= page_size:
                    break
                item = VnfFmAlarmItem(alarm['id'],
                                      alarm['managedObjectId'],
                                      alarm['ackState'],
                                      alarm['eventType'],
                                      alarm['perceivedSeverity'],
                                      alarm['probableCause'])
                rows.append(item)
            return rows
        except Exception:
            self._has_more = False
            error_message = _('Failed to get FM Alarms.')
            exceptions.handle(self.request, error_message)
            return []


class VnfFmAlarmTabs(tabs.TabGroup):
    slug = "vnffmalarm_tabs"
    tabs = (VnfFmAlarmTab,)
    sticky = True


class VnfFmAlarmDetailTab(tabs.Tab):
    name = _("VNF FM Alarm")
    slug = "vnffmalarm_detail_tab"
    template_name = "nfv/vnffmalarm/alarm_detail.html"

    def get_context_data(self, request):
        return {'alarm': self.tab_group.kwargs['alarm']}


class VnfFmAlarmDetailTabs(tabs.TabGroup):
    slug = "vnffmalarm_detail_tabs"
    tabs = (VnfFmAlarmDetailTab,)
    sticky = True
