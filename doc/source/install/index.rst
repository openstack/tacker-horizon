==================
Installation Guide
==================

Manual Installation
-------------------

**Note:** The paths we are using for configuration files in these steps
are with reference to Ubuntu Operating System. The paths may vary for
other Operating Systems.

The branch_name which is used in commands, specify the branch_name
as stable/<branch> for any stable branch installation. For eg:
stable/queens. If unspecified the default will be master branch.

1. Clone tacker-horizon repository.

  ::

    cd ~/
    git clone https://opendev.org/openstack/tacker-horizon -b <branch_name>


2. Install horizon module.

  ::

    cd tacker-horizon
    sudo python3 setup.py install


3. Enable tacker horizon in dashboard.

  ::

    sudo cp tacker_horizon/enabled/* \
        /opt/stack/horizon/openstack_dashboard/enabled/


4. Collect and compress static files.

  ::

    ./manage.py collectstatic --noinput
    echo yes | ./manage.py compress


5. Restart Apache server.

  ::

    sudo systemctl restart apache2


Install via Devstack
--------------------

The tacker-horizon is automatically enabled when tacker server
is installed.

.. seealso::

   https://docs.openstack.org/tacker/latest/install/devstack.html
