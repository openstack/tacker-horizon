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


from django.http import Http404
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import messages
from horizon import tables

from openstack_dashboard import policy
from tacker_horizon.openstack_dashboard import api


class VNFManagerItem(object):

    def __init__(self, name, description, vnfs, vim, status,
                 stack_status, stack_id):
        self.name = name
        self.description = description
        self.vnfs = vnfs
        self.vim = vim
        self.status = status
        self.stack_status = stack_status
        self.id = stack_id


class VNFManagerItemList(object):
    VNFLIST_P = []

    @classmethod
    def get_obj_given_stack_id(cls, vnf_id):
        for obj in cls.VNFLIST_P:
            if obj.id == vnf_id:
                return obj

    @classmethod
    def add_item(cls, item):
        cls.VNFLIST_P.append(item)

    @classmethod
    def clear_list(cls):
        cls.VNFLIST_P = []


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class StacksUpdateRow(tables.Row):
    ajax = True

    def can_be_selected(self, datum):
        return datum.status != 'DELETE_COMPLETE'

    def get_data(self, request, stack_id):
        try:
            stack = api.heat.stack_get(request, stack_id)
            if stack.stack_status == 'DELETE_COMPLETE':
                # returning 404 to the ajax call removes the
                # row from the table on the ui
                raise Http404
            item = VNFManagerItemList.get_obj_given_stack_id(stack_id)
            item.status = stack.status
            item.stack_status = stack.stack_status
            return item
        except Http404:
            raise
        except Exception as e:
            messages.error(request, e)
            raise


class VNFUpdateRow(tables.Row):
    ajax = True

    def can_be_selected(self, datum):
        return datum.status != 'DELETE_COMPLETE'

    def get_data(self, request, vnf_id):
        try:
            # stack = api.heat.stack_get(request, stack_id)
            # if stack.stack_status == 'DELETE_COMPLETE':
                # returning 404 to the ajax call removes the
                # row from the table on the ui
            #    raise Http404
            item = VNFManagerItemList.get_obj_given_stack_id(vnf_id)
            vnf_instance = api.tacker.get_vnf(request, vnf_id)

            if not vnf_instance and not item:
                # TODO(NAME) - bail with error
                return None

            if not vnf_instance and item:
                # API failure, just keep the current state
                return item

            vnf = vnf_instance['vnf']
            try:
                vnf_services_str = vnf['attributes']['service_type']
            except KeyError:
                vnf_services_str = ""
            try:
                vnf_desc_str = vnf['description']
            except KeyError:
                vnf_desc_str = ""

            vim = vnf['placement_attr']['vim_name']
            if not item:
                # Add an item entry
                item = VNFManagerItem(vnf['name'], vnf_desc_str,
                                      vnf_services_str, str(vim),
                                      vnf['status'], vnf['status'], vnf['id'])
            else:
                item.description = vnf_desc_str
                item.vnfs = vnf_services_str
                item.status = vnf['status']
                item.stack_status = vnf['status']
            return item
        except Http404:
            raise
        except Exception as e:
            messages.error(request, e)
            raise


class DeleteVNF(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Terminate VNF",
            u"Terminate VNFs",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Terminate VNF",
            u"Terminate VNFs",
            count
        )

    def action(self, request, obj_id):
        api.tacker.delete_vnf(request, obj_id)


class DeployVNF(tables.LinkAction):
    name = "deployvnf"
    verbose_name = _("Deploy VNF")
    classes = ("ajax-modal",)
    icon = "plus"
    url = "horizon:nfv:vnfmanager:deployvnf"


class VNFManagerTable(tables.DataTable):
    STATUS_CHOICES = (
        ("ACTIVE", True),
        ("ERROR", False),
    )
    STACK_STATUS_DISPLAY_CHOICES = (
        ("init_in_progress", pgettext_lazy("current status of stack",
                                           u"Init In Progress")),
        ("init_complete", pgettext_lazy("current status of stack",
                                        u"Init Complete")),
        ("init_failed", pgettext_lazy("current status of stack",
                                      u"Init Failed")),
        ("create_in_progress", pgettext_lazy("current status of stack",
                                             u"Create In Progress")),
        ("create_complete", pgettext_lazy("current status of stack",
                                          u"Create Complete")),
        ("create_failed", pgettext_lazy("current status of stack",
                                        u"Create Failed")),
        ("delete_in_progress", pgettext_lazy("current status of stack",
                                             u"Delete In Progress")),
        ("delete_complete", pgettext_lazy("current status of stack",
                                          u"Delete Complete")),
        ("delete_failed", pgettext_lazy("current status of stack",
                                        u"Delete Failed")),
        ("update_in_progress", pgettext_lazy("current status of stack",
                                             u"Update In Progress")),
        ("update_complete", pgettext_lazy("current status of stack",
                                          u"Update Complete")),
        ("update_failed", pgettext_lazy("current status of stack",
                                        u"Update Failed")),
        ("rollback_in_progress", pgettext_lazy("current status of stack",
                                               u"Rollback In Progress")),
        ("rollback_complete", pgettext_lazy("current status of stack",
                                            u"Rollback Complete")),
        ("rollback_failed", pgettext_lazy("current status of stack",
                                          u"Rollback Failed")),
        ("suspend_in_progress", pgettext_lazy("current status of stack",
                                              u"Suspend In Progress")),
        ("suspend_complete", pgettext_lazy("current status of stack",
                                           u"Suspend Complete")),
        ("suspend_failed", pgettext_lazy("current status of stack",
                                         u"Suspend Failed")),
        ("resume_in_progress", pgettext_lazy("current status of stack",
                                             u"Resume In Progress")),
        ("resume_complete", pgettext_lazy("current status of stack",
                                          u"Resume Complete")),
        ("resume_failed", pgettext_lazy("current status of stack",
                                        u"Resume Failed")),
        ("adopt_in_progress", pgettext_lazy("current status of stack",
                                            u"Adopt In Progress")),
        ("adopt_complete", pgettext_lazy("current status of stack",
                                         u"Adopt Complete")),
        ("adopt_failed", pgettext_lazy("current status of stack",
                                       u"Adopt Failed")),
        ("snapshot_in_progress", pgettext_lazy("current status of stack",
                                               u"Snapshot In Progress")),
        ("snapshot_complete", pgettext_lazy("current status of stack",
                                            u"Snapshot Complete")),
        ("snapshot_failed", pgettext_lazy("current status of stack",
                                          u"Snapshot Failed")),
        ("check_in_progress", pgettext_lazy("current status of stack",
                                            u"Check In Progress")),
        ("check_complete", pgettext_lazy("current status of stack",
                                         u"Check Complete")),
        ("check_failed", pgettext_lazy("current status of stack",
                                       u"Check Failed")),
    )
    name = tables.Column("name",
                         verbose_name=_("VNF Name"))
    description = tables.Column("description",
                                verbose_name=_("Description"))
    vnfs = tables.Column("vnfs",
                         verbose_name=_("Deployed Services"))
    vim = tables.Column("vim", verbose_name=_("VIM"))
    status = tables.Column("status",
                           hidden=True,
                           status=True,
                           status_choices=STATUS_CHOICES)
    stack_status = tables.Column("stack_status",
                                 verbose_name=_("Status"),
                                 display_choices=STACK_STATUS_DISPLAY_CHOICES)

    class Meta(object):
        name = "vnfmanager"
        verbose_name = _("VNFManager")
        status_columns = ["status", ]
        row_class = VNFUpdateRow
        table_actions = (DeployVNF, DeleteVNF, MyFilterAction,)
