from .blaze import logger as bl
from .iplogger import logger as il
from .conf import USE

class IpLogger(il.IpLogger if USE == 'iplogger' else bl.IpLogger):
    def __init__(self, headless = False, timeout = 10, logger = "blaze"):
        super().__init__(headless = headless, timeout = timeout)