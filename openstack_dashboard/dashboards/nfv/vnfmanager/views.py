from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from horizon import exceptions
from horizon import forms

from horizon.utils import memoized

from openstack_dashboard import api

from openstack_dashboard.dashboards.nfv.vnfmanager \
    import forms as project_forms

from openstack_dashboard.dashboards.nfv.vnfmanager \
    import tabs as nfv_tabs


class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = nfv_tabs.VNFManagerTabs
    template_name = 'nfv/vnfmanager/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class AddServiceView(forms.ModalFormView):
    form_class = project_forms.AddService
    template_name = 'nfv/vnfmanager/add_service.html'
    success_url = reverse_lazy("horizon:nfv:vnfmanager:index")
    modal_id = "add_service_modal"
    modal_header = _("Deploy VNF")
    submit_label = _("Deploy VNF")
    submit_url = "horizon:nfv:vnfmanager:addservice"

    #@memoized.memoized_method
    #def get_object(self):
    #    try:
    #        return api.nova.server_get(self.request,
    #                                   self.kwargs["instance_id"])
    #    except Exception:
    #        exceptions.handle(self.request,
    #                          _("Unable to retrieve instance."))

    def get_initial(self):
        # return {"instance_id": self.kwargs["instance_id"]}
        return {}

    def get_context_data(self, **kwargs):
        context = super(AddServiceView, self).get_context_data(**kwargs)
        # instance_id = self.kwargs['instance_id']
        #context['instance_id'] = instance_id
        # context['instance'] = self.get_object()
        context['submit_url'] = reverse(self.submit_url)
        return context
