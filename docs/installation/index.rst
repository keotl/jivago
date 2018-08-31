Installation
=============

.. toctree::
   :maxdepth: 2

Jivago and its dependencies can be installed from PyPi. Python3.6 or greater is required.

.. code-block:: sh

   pip install jivago


Virtualenv
-----------
Using a virtual environment is recommended for developing and deploying applications.

.. code-block:: sh

   virtualenv -p python3.6 venv
   source venv/bin/activate
   pip install jivago
   pip freeze > requirements.txt


