Deploying Jivago Applications
================================
Jivago implements the WSGI interface for web applications. Therefore, a WSGI server is required for serving requests. While developing, Werkzeug is the recommended WSGI server, as it is easily started and provides convenient debug features.

.. literalinclude:: werkzeug.py
   :language: python


Running in Production
-----------------------
For production purposes, other WSGI servers are available, such as *gunicorn* and *uwsgi*.
See `here <https://github.com/keotl/jivago-heroku-example>`_ for a complete deployment example for heroku.

