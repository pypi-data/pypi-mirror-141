"""PySPOD init"""
__all__ = ['spod_base', 'spod_low_storage', 'spod_low_ram', 'spod_streaming']
# __all__ = ['SPOD_base', 'SPOD_low_storage', 'SPOD_low_ram', 'SPOD_streaming']

from .spod_base        import SPOD_base
from .spod_low_storage import SPOD_low_storage
from .spod_low_ram     import SPOD_low_ram
from .spod_streaming   import SPOD_streaming

# from pyspod import SPOD_low_storage, SPOD_low_ram, SPOD_streaming

import os
import sys
PACKAGE_PARENTS = ['..']
SCRIPT_DIR = os.path.dirname(os.path.realpath(
	os.path.join(os.getcwd(),
	os.path.expanduser(__file__))))
for P in PACKAGE_PARENTS:
	sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, P)))

__project__ = 'PySPOD'
__title__ = "pyspod"
__author__ = "Gianmarco Mengaldo, Romit Maulik, Andrea Lario"
__email__ = 'mpegim@nus.edu.sg, rmaulik@anl.gov, alario@sissa.it'
__copyright__ = "Copyright 2020-2022 PySPOD authors and contributors"
__maintainer__ = __author__
__status__ = "Stable"
__license__ = "MIT"
__version__ = "1.0.0"
__url__ = "https://github.com/mengaldo/PySPOD"
