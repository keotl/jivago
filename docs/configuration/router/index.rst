Router Configuration
======================
The request router is configured in the ``create_router_config()`` method of your application context.

.. literalinclude:: router_context.py
   :language: python

Configuration itself is done by adding new rules to the router builder, using the ``add_rule`` method.

Routing rules
--------------
Each routing rule requires a prefix path which acts as a root path from which requests are served, and a ``RoutingTable`` which contains the actual route definitions. The ``rewrite_path`` parameter defaults to ``True`` and is used to remove the path prefix from the request object before invoking the resource class. 


.. literalinclude:: simple_rules.py
   :language: python


Example : Mapping all routes to the ``/api`` prefix
   ----------------------------------------------------
   To completely override the default *production* or *debug* configuration, omit the *super()* call, and start with a fresh ``RouterBuilder``.

   .. literalinclude:: root_remap.py
      :language: python

   Note the required default rules for proper operation :
     * ``FilteringRule('*', self.get_default_filters())``
         This rule adds all Jivago filters which are required for proper error and serialization handling.
     * ``AutoDiscoveringFilteringRule('*', self.registry, self.root_package_name)``
         This rule registers user-defined request filters using the `@RequestFilter` annotation.
     * ``RoutingRule('/', AutoDiscoveringRoutingTable(self.registry, self.root_package_name))``
         This is where the reflectively declared routes are registered. Without this rule, ``@Resource``, ``@GET, @POST, ...`` annotations will not be parsed. Edit the prefix path to your liking.

Filtering rules
----------------
While additional request filters can be added to all requests by using the ``@RequestFilter`` annotation, specific filtering rules can be added to apply filters to specific routes only. The ``FilteringRule`` rule uses a path pattern which is used to select which filters to apply on any given incoming request. The pattern can either be given using a simple ``*``-style wildcard, or using a regexp pattern.

.. literalinclude:: filter_rules.py
   :language: python

Note that the simple URL pattern parameter is ignored when a regular expression is supplied.

CORS rules
-----------
CORS preflight behaviour can be tuned using CORS rules. The supplied prefix is used to define different behaviours for different sub-paths. The CORS rule does NOT support fuzzy pattern matching like the filtering rule. When multiple rules are applicable to an incoming request, only the longest one is applied. 

.. Literalinclude:: cors_rules.py
   :language: python

**By default, using the ``DebugJivagoContext`` adds a** ``Access-Control-Allow-Origin: *`` **rule at the root of the route hierarchy.**
