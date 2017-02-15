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
