Functional-style operations using Streams
=============================================
Jivago provides a ``Stream`` class which can be used to perform functional-style operations on collections. This mechanism is heavily inspired by *Java*'s identically named *Streams*.

.. literalinclude:: simple_stream.py
   :language: python

In the previous example, the usual *filter* and *map* operations are used in a sequential manner. While all these operations are all available in Python, using Jivago's *Streams* allows the chaining of these operations to improve readability.

All available functions are documented in `jivago.lang.stream`_.

.. _jivago.lang.stream: ../source/jivago.lang.stream.html

Wrapping None values using Nullables
------------------------------------
Jivago provides ``Nullable`` objects which are used to wrap None items. This class follows the same structure as *Java*'s ``Optional`` class. Terminal ``Stream`` operations which return a single item use this mechanism.

All available functions are documented in `jivago.lang.nullable`_.

.. _jivago.lang.nullable: ../source/jivago.lang.nullable.html

Other examples
---------------
.. literalinclude:: other_examples.py
   :language: python
