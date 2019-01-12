Manual Route Registration
==================

.. toctree::
   :maxdepth: 2


Additionnal URL routes can be registered by creating a new ``RoutingTable`` which references classes and their methods. Note that the appropriate classes should be imported beforehand. The referenced resource class can be either an instance, or the actual class. In that case, it will be instantiated by the ServiceLocator, and should therefore be registered manually in the ``configure_service_locator`` context method.

.. literalinclude:: routing_table.py
   :language: python

This new ``RoutingTable`` can then be used to configure the ``Router`` object, which is used to serve all requests. The recommended way of configuring your application is by inheriting from the ``ProductionJivagoContext`` class, and then overriding the ``create_router_config`` method.

.. literalinclude:: router_config.py
   :language: python

Serving static files
--------------------
While it is not generally recommended to serve static files from a WSGI application for performance reasons, Jivago supports static file serving. The ``StaticFileRoutingTable`` dynamically defines routes for serving files.

.. literalinclude:: static.py
   :language: python

The ``StaticFileRoutingTable`` can also be used with a ``allowed_extensions`` parameter to explicitly allow or disallow specific file types.



Additional router configuration options, including specific filter and CORS rules, can be found at `Router Configuration`_.

.. _Router Configuration: ../configuration/router/index.html
