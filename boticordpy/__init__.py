"""
Boticord API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the BotiCord API.
:copyright: (c) 2022 Marakarka
:license: MIT, see LICENSE for more details.
"""

__title__ = "boticordpy"
__author__ = "Marakarka"
__license__ = "MIT"
__copyright__ = "Copyright 2022 Marakarka"
__version__ = "2.1.0"

from .client import BoticordClient
from .webhook import Webhook

from .types import *
