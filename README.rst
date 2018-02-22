========================
Team and repository tags
========================

.. image:: http://governance.openstack.org/badges/tacker-horizon.svg
          :target: http://governance.openstack.org/reference/tags/index.html

.. Change things from this point on


Tacker Horizon UI
=================

Horizon UI for Tacker VNF Manager

Installation
============

**Note:** The paths we are using for configuration files in these steps
are with reference to Ubuntu Operating System. The paths may vary for
other Operating Systems.

The branch_name which is used in commands, specify the branch_name
as stable/<branch> for any stable branch installation. For eg:
stable/queens, stable/pike. If unspecified the default will be
master branch.

1. Clone tacker-horizon repository.

  ::

    cd ~/
    git clone https://github.com/openstack/tacker-horizon -b <branch_name>


2. Install horizon module.

  ::

    cd tacker-horizon
    sudo python setup.py install


3. Enable tacker horizon in dashboard.

  ::

    sudo cp tacker_horizon/enabled/* \
        /opt/stack/horizon/openstack_dashboard/enabled/


4. Restart Apache server.

  ::

    sudo service apache2 restart


More Information
================

[1] Tacker Documentation: https://docs.openstack.org/tacker/
[2] Tacker Wiki: https://wiki.openstack.org/wiki/Tacker
