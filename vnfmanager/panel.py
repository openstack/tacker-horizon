from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.nfv import dashboard

class Vnfmanager(horizon.Panel):
    name = _("VNF Manager")
    slug = "vnfmanager"


dashboard.Nfv.register(Vnfmanager)
