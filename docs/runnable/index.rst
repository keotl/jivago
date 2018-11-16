Runnable Components
=====================

.. toctree::
   :maxdepth: 2

Jivago provides a mechanism for running background tasks and exposes application initialization hooks. For both of those purposes, the ``Runnable`` interface is used. 

.. literalinclude:: runnable.py
   :language: python


Background Workers
--------------------
For running continuous tasks on a background thread, use the ``@BackgroundWorker`` annotation. These components will be started on separate threads when the app has started successfully. Components instantiated in this manner support all of the usual dependency injection features.

.. literalinclude:: background_worker.py
   :language: python

Application Initialization Hooks
------------------------------------
``@PreInit``, ``@Init`` and ``@PostInit`` hooks are provided for running one-off tasks at startup and are invoked identically to background workers. These are, however, required to exit before the application can start.

.. literalinclude:: app_init_hooks.py
   :language: python



* **PreInit** is invoked right after the service locator and application properties are configured.
* **Init** is invoked after initializing the routing table. At this stage, the application is in a coherent state.
* **PostInit** is invoked after starting background workers and scheduled tasks. No further initialization task is left to be done.


Scheduled Tasks
-----------------
One-off background tasks can be scheduled over a longer period of time using scheduled tasks. The ``@Scheduled`` annotation takes either a "cron" or "every" parameter.

* ``cron`` : Takes a cron-style string.
* ``every``: Takes a *Duration* enum. (Duration.SECOND, Duration.MINUTE, Duration.HOUR, Duration.DAY)
* ``start`` : *Optional*. Specifies a start time before which the task will not be run.

.. literalinclude:: scheduled.py
   :language: python


