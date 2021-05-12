#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from openstack_dashboard.test.integration_tests import helpers


class TestTackerDashboardInstalled(helpers.TestCase):

    def test_vnf_catalog_page_opened(self):
        vnf_catalog = self.home_pg.go_to_nfv_vnfmanagement_vnfcatalogpage()
        self.assertEqual(vnf_catalog.page_title,
                         'VNF Catalog - OpenStack Dashboard')

    def test_vnf_manager_page_opened(self):
        vnf_manager = self.home_pg.go_to_nfv_vnfmanagement_vnfmanagerpage()
        self.assertEqual(vnf_manager.page_title,
                         'VNF Manager - OpenStack Dashboard')

    def test_vim_page_opened(self):
        vim = self.home_pg.go_to_nfv_nfvorchestration_vimmanagementpage()
        self.assertEqual(vim.page_title,
                         'VIM - OpenStack Dashboard')

    def test_vnffg_catalog_page_opened(self):
        vnffg_catalog = (
                self.home_pg.go_to_nfv_nfvorchestration_vnffgcatalogpage())
        self.assertEqual(vnffg_catalog.page_title,
                         'VNFFG Catalog - OpenStack Dashboard')

    def test_vnffg_manager_page_opened(self):
        vnffg_manager = (
                self.home_pg.go_to_nfv_nfvorchestration_vnffgmanagerpage())
        self.assertEqual(vnffg_manager.page_title,
                         'VNFFG Manager - OpenStack Dashboard')

    def test_ns_catalog_page_opened(self):
        ns_catalog = self.home_pg.go_to_nfv_nfvorchestration_nscatalogpage()
        self.assertEqual(ns_catalog.page_title,
                         'NS Catalog - OpenStack Dashboard')

    def test_ns_manager_page_opened(self):
        ns_manager = self.home_pg.go_to_nfv_nfvorchestration_nsmanagerpage()
        self.assertEqual(ns_manager.page_title,
                         'NS Manager - OpenStack Dashboard')
