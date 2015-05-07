from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.nfv import dashboard

class Vnfcatalog(horizon.Panel):
    name = _("VNF Catalog")
    slug = "vnfcatalog"


dashboard.Nfv.register(Vnfcatalog)
