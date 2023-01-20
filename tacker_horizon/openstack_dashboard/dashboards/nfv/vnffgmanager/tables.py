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
from django.utils.translation import pgettext_lazy

from horizon import messages
from horizon import tables

from openstack_dashboard import policy
from tacker_horizon.openstack_dashboard import api
from tackerclient.common.exceptions import NotFound


class VNFFGManagerItem(object):
    def __init__(self, id, name, description, status):
        self.id = id
        self.name = name
        self.description = description
        self.status = status


class VNFFGManagerItemList(object):
    VNFFGLIST_P = []

    @classmethod
    def get_obj_given_id(cls, vnffg_id):
        for obj in cls.VNFFGLIST_P:
            if obj.id == vnffg_id:
                return obj

    @classmethod
    def add_item(cls, item):
        cls.VNFFGLIST_P.append(item)

    @classmethod
    def clear_list(cls):
        cls.VNFFGLIST_P = []


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class VNFFGUpdateRow(tables.Row):
    ajax = True

    def can_be_selected(self, datum):
        return datum.status != 'DELETE_COMPLETE'

    def get_data(self, request, vnffg_id):
        try:
            item = VNFFGManagerItemList.get_obj_given_id(vnffg_id)
            vnffg_instance = api.tacker.get_vnffg(request, vnffg_id)

            if not vnffg_instance and not item:
                # TODO(NAME) - bail with error
                return None

            if not vnffg_instance and item:
                # API failure, just keep the current state
                return item

            vnffg = vnffg_instance['vnffg']
            try:
                vnffg_desc_str = vnffg['description']
            except KeyError:
                vnffg_desc_str = ""

            if not item:
                # Add an item entry
                item = VNFFGManagerItem(vnffg['name'], vnffg_desc_str,
                                        vnffg['status'], vnffg['id'])
            else:
                item.description = vnffg_desc_str
                item.status = vnffg['status']
            return item
        except (Http404, NotFound):
            raise Http404
        except Exception as e:
            messages.error(request, e)
            raise


class DeleteVNFFG(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Terminate VNFFG",
            "Terminate VNFFGs",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Terminate VNFFG",
            "Terminate VNFFGs",
            count
        )

    def action(self, request, obj_id):
        api.tacker.delete_vnffg(request, obj_id)


class DeployVNFFG(tables.LinkAction):
    name = "deployvnffg"
    verbose_name = _("Deploy VNFFG")
    classes = ("ajax-modal",)
    icon = "plus"
    url = "horizon:nfv:vnffgmanager:deployvnffg"


class VNFFGManagerTable(tables.DataTable):
    STATUS_CHOICES = (
        ("ACTIVE", True),
        ("ERROR", False),
    )
    STACK_STATUS_DISPLAY_CHOICES = (
        ("init_in_progress", pgettext_lazy("current status of stack",
                                           "Init In Progress")),
        ("init_complete", pgettext_lazy("current status of stack",
                                        "Init Complete")),
        ("init_failed", pgettext_lazy("current status of stack",
                                      "Init Failed")),
        ("create_in_progress", pgettext_lazy("current status of stack",
                                             "Create In Progress")),
        ("create_complete", pgettext_lazy("current status of stack",
                                          "Create Complete")),
        ("create_failed", pgettext_lazy("current status of stack",
                                        "Create Failed")),
        ("delete_in_progress", pgettext_lazy("current status of stack",
                                             "Delete In Progress")),
        ("delete_complete", pgettext_lazy("current status of stack",
                                          "Delete Complete")),
        ("delete_failed", pgettext_lazy("current status of stack",
                                        "Delete Failed")),
        ("update_in_progress", pgettext_lazy("current status of stack",
                                             "Update In Progress")),
        ("update_complete", pgettext_lazy("current status of stack",
                                          "Update Complete")),
        ("update_failed", pgettext_lazy("current status of stack",
                                        "Update Failed")),
        ("rollback_in_progress", pgettext_lazy("current status of stack",
                                               "Rollback In Progress")),
        ("rollback_complete", pgettext_lazy("current status of stack",
                                            "Rollback Complete")),
        ("rollback_failed", pgettext_lazy("current status of stack",
                                          "Rollback Failed")),
        ("suspend_in_progress", pgettext_lazy("current status of stack",
                                              "Suspend In Progress")),
        ("suspend_complete", pgettext_lazy("current status of stack",
                                           "Suspend Complete")),
        ("suspend_failed", pgettext_lazy("current status of stack",
                                         "Suspend Failed")),
        ("resume_in_progress", pgettext_lazy("current status of stack",
                                             "Resume In Progress")),
        ("resume_complete", pgettext_lazy("current status of stack",
                                          "Resume Complete")),
        ("resume_failed", pgettext_lazy("current status of stack",
                                        "Resume Failed")),
        ("adopt_in_progress", pgettext_lazy("current status of stack",
                                            "Adopt In Progress")),
        ("adopt_complete", pgettext_lazy("current status of stack",
                                         "Adopt Complete")),
        ("adopt_failed", pgettext_lazy("current status of stack",
                                       "Adopt Failed")),
        ("snapshot_in_progress", pgettext_lazy("current status of stack",
                                               "Snapshot In Progress")),
        ("snapshot_complete", pgettext_lazy("current status of stack",
                                            "Snapshot Complete")),
        ("snapshot_failed", pgettext_lazy("current status of stack",
                                          "Snapshot Failed")),
        ("check_in_progress", pgettext_lazy("current status of stack",
                                            "Check In Progress")),
        ("check_complete", pgettext_lazy("current status of stack",
                                         "Check Complete")),
        ("check_failed", pgettext_lazy("current status of stack",
                                       "Check Failed")),
    )
    name = tables.Column("name",
                         link="horizon:nfv:vnffgmanager:detail",
                         verbose_name=_("VNFFG Name"))
    description = tables.Column("description",
                                verbose_name=_("Description"))
    status = tables.Column("status",
                           hidden=False,
                           status=True,
                           status_choices=STATUS_CHOICES)

    class Meta(object):
        name = "vnffgmanager"
        verbose_name = _("VNFFGManager")
        status_columns = ["status", ]
        row_class = VNFFGUpdateRow
        table_actions = (DeployVNFFG, DeleteVNFFG, MyFilterAction,)
