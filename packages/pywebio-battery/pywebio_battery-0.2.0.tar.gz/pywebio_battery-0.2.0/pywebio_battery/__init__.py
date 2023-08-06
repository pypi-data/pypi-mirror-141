"""
``pywebio_battery`` --- PyWebIO battery
=========================================

*Utilities that help write PyWebIO apps quickly and easily.*

Functions list
-----------------

.. list-table::

   * - Function name
     - Description

   * - `confirm <pywebio_battery.confirm>`
     - Confirmation modal



"""
from .interaction import *
from .web import *
from .interaction import __all__ as interaction_all
from .web import __all__ as web_all

__all__ = interaction_all + web_all

# Set default logging handler to avoid "No handler found" warnings.
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
del logging
