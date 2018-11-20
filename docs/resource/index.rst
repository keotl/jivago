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
