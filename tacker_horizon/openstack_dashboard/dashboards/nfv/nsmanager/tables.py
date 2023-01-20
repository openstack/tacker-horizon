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


from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

from horizon import messages
from horizon import tables

from openstack_dashboard import policy
from tacker_horizon.openstack_dashboard import api
from tackerclient.common.exceptions import NotFound


class NSManagerItem(object):
    def __init__(self, name, description, vim, status,
                 ns_id, error_reason):
        self.name = name
        self.description = description
        self.vim = vim
        self.status = status
        self.id = ns_id
        self.error_reason = error_reason


class NSManagerItemList(object):
    NSLIST_P = []

    @classmethod
    def get_obj_given_stack_ids(cls, ns_id):
        for obj in cls.NSLIST_P:
            if obj.id == ns_id:
                return obj

    @classmethod
    def add_item(cls, item):
        cls.NSLIST_P.append(item)

    @classmethod
    def clear_list(cls):
        cls.NSLIST_P = []


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class NSUpdateRow(tables.Row):
    ajax = True

    def can_be_selected(self, datum):
        return datum.status != 'DELETE_COMPLETE'

    def get_data(self, request, ns_id):
        try:
            # stack = api.heat.stack_get(request, stack_id)
            # if stack.stack_status == 'DELETE_COMPLETE':
            # returning 404 to the ajax call removes the
            # row from the table on the ui
            #    raise Http404
            item = NSManagerItemList.get_obj_given_stack_ids(ns_id)
            ns_instance = api.tacker.get_ns(request, ns_id)

            if not ns_instance and not item:
                # TODO(NAME) - bail with error
                return None

            if not ns_instance and item:
                # API failure, just keep the current state
                return item

            ns = ns_instance['ns']
            try:
                ns_desc_str = ns['description']
            except KeyError:
                ns_desc_str = ""

            vim = ns['vim_id']
            if not item:
                # Add an item entry
                item = NSManagerItem(ns['name'], ns_desc_str,
                                     str(vim),
                                     ns['status'], ns['id'],
                                     ns['error_reason'])
            else:
                item.description = ns_desc_str
                item.status = ns['status']
                item.id = ns['id']
            return item
        except (Http404, NotFound):
            raise Http404
        except Exception as e:
            messages.error(request, e)
            raise


class DeleteNS(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Terminate NS",
            "Terminate NSs",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Terminate NS",
            "Terminate NSs",
            count
        )

    def action(self, request, obj_id):
        api.tacker.delete_ns(request, obj_id)


class DeployNS(tables.LinkAction):
    name = "deployns"
    verbose_name = _("Deploy NS")
    classes = ("ajax-modal",)
    icon = "plus"
    url = "horizon:nfv:nsmanager:deployns"


class NSManagerTable(tables.DataTable):
    STATUS_CHOICES = (
        ("ACTIVE", True),
        ("ERROR", False),
    )
    name = tables.Column("name",
                         link="horizon:nfv:nsmanager:detail",
                         verbose_name=_("NS Name"))
    description = tables.Column("description",
                                verbose_name=_("Description"))
    vim = tables.Column("vim", verbose_name=_("VIM"))
    status = tables.Column("status",
                           status=True,
                           status_choices=STATUS_CHOICES)
    error_reason = tables.Column("error_reason",
                                 verbose_name=_("Error Reason"))

    class Meta(object):
        name = "nsmanager"
        verbose_name = _("NSManager")
        status_columns = ["status", ]
        row_class = NSUpdateRow
        table_actions = (DeployNS, DeleteNS, MyFilterAction,)
