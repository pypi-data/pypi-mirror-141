"""
``pywebio.pin`` --- PyWebIO battery
======================================

*Utilities that help write PyWebIO apps quickly and easily.*

.. automodule:: pywebio-battery.io
.. automodule:: pywebio-battery.web
"""
from .io import *
from .web import *

# Set default logging handler to avoid "No handler found" warnings.
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
del logging