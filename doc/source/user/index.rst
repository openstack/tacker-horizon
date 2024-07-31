==========
User Guide
==========

**Reference:** https://docs.openstack.org/tacker/latest/user/index.html


Support APIs
------------

Tacker Horizon supports the following APIs:

**Supported Legacy APIs**

.. list-table:: `VIM Management`_
  :widths: 5 9 4
  :header-rows: 1

  * - API name
    - Method & URI
    - ETSI NFV-SOL Version
  * - Register VIM
    - POST /v1.0/vims
    - None
  * - List VIMs
    - GET /v1.0/vims
    - None
  * - Delete VIM
    - Delete /v1.0/vims/{vim_id}
    - None


.. warning::

  Some Legacy API functions other than VIM Management are displayed,
  but those APIs have been removed and cannot be used.


**Supported v1 APIs**

.. list-table:: `VNF Package Management`_
  :widths: 5 9 4
  :header-rows: 1

  * - API name
    - Method & URI
    - ETSI NFV-SOL Version
  * - Create VNF Package
    - POST /vnfpkgm/v1/vnf_packages
    - `ETSI NFV-SOL004 2.6.1`_ `ETSI NFV-SOL005 2.6.1`_
  * - List VNF Packages
    - GET /vnfpkgm/v1/vnf_packages
    - `ETSI NFV-SOL004 2.6.1`_ `ETSI NFV-SOL005 2.6.1`_
  * - Show VNF Package
    - GET /vnfpkgm/v1/vnf_packages/{vnf_package_id}
    - `ETSI NFV-SOL004 2.6.1`_ `ETSI NFV-SOL005 2.6.1`_
  * - Delete VNF Package
    - Delete /vnfpkgm/v1/vnf_packages/{vnf_package_id}
    - `ETSI NFV-SOL004 2.6.1`_ `ETSI NFV-SOL005 2.6.1`_
  * - Upload VNF Package from content
    - PUT /vnfpkgm/v1/vnf_packages/{vnf_package_id}/
      package_content
    - `ETSI NFV-SOL004 2.6.1`_ `ETSI NFV-SOL005 2.6.1`_
  * - Upload VNF Package from uri
    - POST /vnfpkgm/v1/vnf_packages/{vnf_package_id}/
      package_content/upload_from_uri
    - `ETSI NFV-SOL004 2.6.1`_ `ETSI NFV-SOL005 2.6.1`_
  * - Update VNF Package Information
    - PATCH /vnfpkgm/v1/vnf_packages/{vnf_package_id}
    - `ETSI NFV-SOL004 2.6.1`_ `ETSI NFV-SOL005 2.6.1`_
  * - Fetch an on-boarded VNF package with HTTP_RANGE
    - GET /vnfpkgm/v1/vnf_packages/{vnf_package_id}/
      package_content
    - `ETSI NFV-SOL004 2.6.1`_ `ETSI NFV-SOL005 2.6.1`_


.. note::

  v1 VNF Lifecycle Management is not supported.

  Please note that when `Create VNF Identifier` is executed
  from VNF Package v1, v2 VNF Instance is created instead of
  v1 VNF Instance.


**Supported v2 APIs**

.. list-table:: `v2 VNF Lifecycle Management`_
  :widths: 5 9 4
  :header-rows: 1

  * - API name
    - Method & URI
    - ETSI NFV-SOL Version
  * - Create a new VNF instance resource (v2)
    - POST /vnflcm/v2/vnf_instances
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Instantiate a VNF instance (v2)
    - POST /vnflcm/v2/vnf_instances/{vnfInstanceId}/instantiate
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Terminate a VNF instance (v2)
    - POST /vnflcm/v2/vnf_instances/{vnfInstanceId}/terminate
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Heal a VNF instance (v2)
    - POST /vnflcm/v2/vnf_instances/{vnfInstanceId}/heal
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Delete a VNF instance (v2)
    - DELETE /vnflcm/v2/vnf_instances/{vnfInstanceId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Show VNF instance (v2)
    - GET /vnflcm/v2/vnf_instances/{vnfInstanceId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - List VNF instance (v2)
    - GET /vnflcm/v2/vnf_instances
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Scale a VNF instance (v2)
    - POST /vnflcm/v2/vnf_instances/{vnfInstanceId}/scale
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Update a VNF instance (v2)
    - PATCH vnflcm/v2/vnf_instances/{vnfInstanceId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Change External VNF Connectivity (v2)
    - POST /vnflcm/v2/vnf_instances/{vnfInstanceId}/change_ext_conn
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Change Current VNF Package (v2)
    - POST /vnflcm/v2/vnf_instances/{vnfInstanceId}/change_vnfpkg
    - `ETSI NFV-SOL002 3.3.1`_ (\*1) `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Show VNF LCM operation occurrence (v2)
    - GET /vnflcm/v2/vnf_lcm_op_occs/{vnfLcmOpOccId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - List VNF LCM operation occurrence (v2)
    - GET /vnflcm/v2/vnf_lcm_op_occs
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Retry a VNF LCM operation occurrence (v2)
    - POST /vnflcm/v2/vnf_lcm_op_occs/{vnfLcmOpOccId}/retry
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Fail a VNF LCM operation occurrence (v2)
    - POST /vnflcm/v2/vnf_lcm_op_occs/{vnfLcmOpOccId}/fail
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Rollback a VNF LCM operation occurrence (v2)
    - POST /vnflcm/v2/vnf_lcm_op_occs/{vnfLcmOpOccId}/rollback
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Create a new subscription (v2)
    - POST /vnflcm/v2/subscriptions
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_ (\*2)
  * - Delete a subscription (v2)
    - DELETE /vnflcm/v2/subscriptions/{subscriptionId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Show subscription (v2)
    - GET /vnflcm/v2/subscriptions/{subscriptionId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - List subscription (v2)
    - GET /vnflcm/v2/subscriptions
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_


(\*1)The functionality related to VNF LCM Coordination in
Change current VNF package complies with `ETSI NFV-SOL002 3.6.1`_.

(\*2)OAUTH2_CLIENT_CERT in SubscriptionAuthentication is compliant with
`ETSI NFV-SOL013 3.5.1`_.


.. list-table:: `VNF Performance Management`_
  :widths: 5 9 4
  :header-rows: 1

  * - API name
    - Method & URI
    - ETSI NFV-SOL Version
  * - Create a PM job (v2)
    - POST /vnfpm/v2/pm_jobs
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_ (\*1)
  * - Get for PM jobs (v2)
    - GET /vnfpm/v2/pm_jobs
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Get a PM job (v2)
    - GET /vnfpm/v2/pm_jobs/{pmJobId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Modify a PM job(v2)
    - PATCH /vnfpm/v2/pm_jobs/{pmJobId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Delete a PM job (v2)
    - DELETE /vnfpm/v2/pm_jobs/{pmJobId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Get individual performance report (v2)
    - GET /vnfpm/v2/pm_jobs/{pmJobId}/reports/{reportId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Create a PM threshold (v2)
    - POST /vnfpm/v2/thresholds
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_ (\*1)
  * - Get for PM thresholds (v2)
    - GET /vnfpm/v2/thresholds
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Get a PM threshold (v2)
    - GET /vnfpm/v2/thresholds/{thresholdId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Modify a PM threshold(v2)
    - PATCH /vnfpm/v2/thresholds/{thresholdId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Delete a PM threshold (v2)
    - DELETE /vnfpm/v2/thresholds/{thresholdId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_


(\*1)OAUTH2_CLIENT_CERT in SubscriptionAuthentication is compliant with
`ETSI NFV-SOL013 3.5.1`_.


.. list-table:: `VNF Fault Management`_
  :widths: 5 9 4
  :header-rows: 1

  * - API name
    - Method & URI
    - ETSI NFV-SOL Version
  * - Get all alarms (v1)
    - GET /vnffm/v1/alarms
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Get the individual alarm (v1)
    - GET /vnffm/v1/alarms/{alarmId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Modify the confirmation status (v1)
    - PATCH /vnffm/v1/alarms/{alarmId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Create a subscription (v1)
    - POST /vnffm/v1/subscriptions
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_ (\*1)
  * - Get all subscriptions (v1)
    - GET /vnffm/v1/subscriptions
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Get a subscription (v1)
    - GET /vnffm/v1/subscriptions/{subscriptionId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_
  * - Delete a subscription (v1)
    - DELETE /vnffm/v1/subscriptions/{subscriptionId}
    - `ETSI NFV-SOL002 3.3.1`_ `ETSI NFV-SOL003 3.3.1`_
      `ETSI NFV-SOL013 3.4.1`_


(\*1)OAUTH2_CLIENT_CERT in SubscriptionAuthentication is compliant with
`ETSI NFV-SOL013 3.5.1`_.


.. _ETSI NFV-SOL002 2.6.1:
  https://www.etsi.org/deliver/etsi_gs/NFV-SOL/001_099/002/02.06.01_60/gs_nfv-sol002v020601p.pdf
.. _ETSI NFV-SOL002 3.3.1:
  https://www.etsi.org/deliver/etsi_gs/NFV-SOL/001_099/002/03.03.01_60/gs_nfv-sol002v030301p.pdf
.. _ETSI NFV-SOL002 3.6.1:
  https://www.etsi.org/deliver/etsi_gs/NFV-SOL/001_099/002/03.06.01_60/gs_nfv-sol002v030601p.pdf
.. _ETSI NFV-SOL003 2.6.1:
  https://www.etsi.org/deliver/etsi_gs/NFV-SOL/001_099/003/02.06.01_60/gs_nfv-sol003v020601p.pdf
.. _ETSI NFV-SOL003 3.3.1:
  https://www.etsi.org/deliver/etsi_gs/NFV-SOL/001_099/003/03.03.01_60/gs_nfv-sol003v030301p.pdf
.. _ETSI NFV-SOL004 2.6.1:
  https://www.etsi.org/deliver/etsi_gs/NFV-SOL/001_099/004/02.06.01_60/gs_nfv-sol004v020601p.pdf
.. _ETSI NFV-SOL005 2.6.1:
  https://www.etsi.org/deliver/etsi_gs/NFV-SOL/001_099/005/02.06.01_60/gs_nfv-sol005v020601p.pdf
.. _ETSI NFV-SOL013 3.4.1:
  https://www.etsi.org/deliver/etsi_gs/NFV-SOL/001_099/013/03.04.01_60/gs_nfv-sol013v030401p.pdf
.. _ETSI NFV-SOL013 3.5.1:
  https://www.etsi.org/deliver/etsi_gs/NFV-SOL/001_099/013/03.05.01_60/gs_nfv-sol013v030501p.pdf
.. _VIM Management:
  https://docs.openstack.org/api-ref/nfv-orchestration/v1/legacy.html
.. _VNF Package Management:
  https://docs.openstack.org/api-ref/nfv-orchestration/v1/vnfpkgm.html
.. _v1 VNF Lifecycle Management:
  https://docs.openstack.org/api-ref/nfv-orchestration/v1/vnflcm.html
.. _v2 VNF Lifecycle Management:
  https://docs.openstack.org/api-ref/nfv-orchestration/v2/vnflcm.html
.. _VNF Performance Management:
  https://docs.openstack.org/api-ref/nfv-orchestration/v2/vnfpm.html
.. _VNF Fault Management:
  https://docs.openstack.org/api-ref/nfv-orchestration/v2/vnffm.html
