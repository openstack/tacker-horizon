========================
Team and repository tags
========================

.. image:: https://governance.openstack.org/tc/badges/tacker-horizon.svg
          :target: https://governance.openstack.org/tc/reference/tags/index.html

.. Change things from this point on


Tacker Horizon UI
=================

Horizon UI for Tacker VNF Manager

Installation
============

1. Install module

  ::

    sudo python setup.py install


2. Copy files to Horizon tree

  ::

    cp tacker_horizon/enabled/* /opt/stack/horizon/openstack_dashboard/enabled/


3. Restart the apache webserver

  ::

    sudo service apache2 restart


More Information
================

Tacker Wiki:
https://wiki.openstack.org/wiki/Tacker
