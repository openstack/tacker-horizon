========================
Team and repository tags
========================

.. image:: https://governance.openstack.org/tc/badges/tacker-horizon.svg
          :target: https://governance.openstack.org/tc/reference/tags/index.html

.. Change things from this point on

Tacker Horizon UI
=================

Horizon UI for Tacker VNF Manager

* License: Apache license
* Source: https://opendev.org/openstack/tacker-horizon
* Bugs: https://bugs.launchpad.net/tacker
* Tacker-horizon docs: https://docs.openstack.org/tacker-horizon/latest/

Installation
============

**Note:** The paths we are using for configuration files in these steps
are with reference to Ubuntu Operating System. The paths may vary for
other Operating Systems.

The branch_name which is used in commands, specify the branch_name
as stable/<branch> for any stable branch installation. For eg:
stable/queens, stable/pike. If unspecified the default will be
master branch. The installation of tacker-horizon is as following
steps.

Clone tacker-horizon repository.
   ::

     cd ~/
     git clone https://opendev.org/openstack/tacker-horizon -b <branch_name>

Install horizon module.
   ::

     cd tacker-horizon
     sudo python setup.py install

Enable tacker horizon in dashboard.
   ::

     sudo cp tacker_horizon/enabled/* \
         /opt/stack/horizon/openstack_dashboard/enabled/

Collect and compress static files.
   ::

     ./manage.py collectstatic --noinput
     echo yes | ./manage.py compress

Restart Apache server using Upstart.
   ::

     sudo service apache2 restart

Or restart Apache server using Systemd.
   ::

     sudo systemctl restart apache2

