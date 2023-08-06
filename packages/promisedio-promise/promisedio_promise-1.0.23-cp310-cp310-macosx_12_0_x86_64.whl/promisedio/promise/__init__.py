import os
import sys

if os.environ.get("PROMISEDIO_DEBUG"):
    from . import _promise_debug
    sys.modules[f"{__name__}._promise"] = _promise_debug

from . _promise import *
del os, sys
