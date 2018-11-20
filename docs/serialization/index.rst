Serialization
===========

.. toctree::
   :maxdepth: 2

Jivago provides an ``ObjectMapper`` object which can be used to serialize and deserialize complex objects. Mapped classes do not need to be annotated with the ``@Serializable`` annotation.

*object_mapper.py*

.. literalinclude:: object_mapper.py
   :language: python

If a constructor (``__init__``) function is declared on the mapped class, parameters are injected, otherwise parameters are set using the ``__setattr__`` method.

