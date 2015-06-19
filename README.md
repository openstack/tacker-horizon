# Tacker Horizon UI 

Horizon UI for Tacker VNF Manager

Installation
------------

1. Install module

    ```
    sudo python setup.py install
    ```

2. Copy files to Horizon tree

    ```
    cp openstack_dashboard_extensions/* /opt/stack/horizon/openstack_dashboard/enabled/
    ```

3. Restart the apache webserver

    ```
    sudo service apache2 restart
    ```

More Information
----------------

https://wiki.openstack.org/wiki/Tacker
