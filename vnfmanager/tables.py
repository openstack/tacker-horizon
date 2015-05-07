from django.utils.translation import ugettext_lazy as _

from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class AddServicesLink(tables.LinkAction):
    name = "addservice"
    verbose_name = _("Deploy VNF")
    classes = ("ajax-modal",)
    icon = "plus"
    url = "horizon:nfv:vnfmanager:addservice"


class VNFManagerTable(tables.DataTable):
    name = tables.Column('name', \
                         verbose_name=_("Compute Nodes"))
    description = tables.Column('description', \
                           verbose_name=_("Description"))
    vnfs = tables.Column('vnfs', \
                         verbose_name=_("Deployed VNFs"))
    status = tables.Column('status', \
                               verbose_name=_("Status"))

    class Meta:
        name = "vnfmanager"
        verbose_name = _("VNFManager")
        table_actions = (AddServicesLink, MyFilterAction,)
