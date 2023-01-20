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

from horizon import tables


class EventItem(object):
    def __init__(self, id, state, type, timestamp, details):
        self.id = id
        self.resource_state = state
        self.event_type = type
        self.timestamp = timestamp
        self.event_details = details


class EventItemList(object):
    EVTLIST_P = []

    @classmethod
    def add_item(cls, item):
        cls.EVTLIST_P.append(item)

    @classmethod
    def clear_list(cls):
        cls.EVTLIST_P = []


class EventsTable(tables.DataTable):

    id = tables.Column('id', verbose_name=_("Event ID"))
    resource_state = tables.Column('resource_state',
                                   verbose_name=_("Resource State"))
    timestamp = tables.Column('timestamp',
                              verbose_name=_("Time Since Event"))
    event_type = tables.Column("event_type", verbose_name=_("Event Type"))
    event_details = tables.Column("event_details",
                                  verbose_name=_("Event Details"))

    class Meta(object):
        name = "events"
