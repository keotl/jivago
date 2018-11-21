Manual Route Registration
==================

.. toctree::
   :maxdepth: 2


Additionnal URL routes can be registered by creating a new ``RoutingTable`` which references classes and their methods. Note that the appropriate classes should be imported beforehand.

.. literalinclude:: routing_table.py
   :language: python

This new ``RoutingTable`` can then be used to configure the ``Router`` object, which is used to serve all requests. The recommended way of configuring your application is by inheriting from the ``ProductionJivagoContext`` class, and then overriding the ``create_router`` method.

.. literalinclude:: router_config.py
   :language: python

Serving static files
--------------------
While it is not generally recommended to serve static files from a WSGI application for performance reasons, Jivago supports static file serving. The ``StaticFileRoutingTable`` dynamically defines routes for serving files.

.. literalinclude:: static.py
   :language: python

The ``StaticFileRoutingTable`` can also be used with a ``allowed_extensions`` parameter to explicitly allow or disallow specific file types.

Defining path prefixes
----------------------
When registering a new routing table, using the ``path_prefix`` parameter maps the new routing table to part of the path hierarchy. For instance, static files can be served from ``/static/my_file.html``.

.. literalinclude:: path_prefix.py
   :language: python
