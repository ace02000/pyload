# -*- coding: utf-8 -*-

from module.plugins.internal.Plugin import set_cookie
from module.plugins.internal.SimpleCrypter import SimpleCrypter, create_getInfo


class XFSCrypter(SimpleCrypter):
    __name__    = "XFSCrypter"
    __type__    = "crypter"
    __version__ = "0.15"
    __status__  = "testing"

    __pattern__ = r'^unmatchable$'

    __description__ = """XFileSharing decrypter plugin"""
    __license__     = "GPLv3"
    __authors__     = [("Walter Purcaro", "vuolter@gmail.com")]


    PLUGIN_DOMAIN = None

    URL_REPLACEMENTS = [(r'&?per_page=\d+', ""), (r'[?/&]+$', ""), (r'(.+/[^?]+)$', r'\1?'), (r'$', r'&per_page=10000')]

    NAME_PATTERN = r'<[Tt]itle>.*?\: (?P<N>.+) folder</[Tt]itle>'
    LINK_PATTERN = r'<(?:td|TD).*?>\s*(?:<.+>\s*)?<a href="(.+?)".*?>.+?(?:</a>)?\s*(?:<.+>\s*)?</(?:td|TD)>'

    OFFLINE_PATTERN      = r'>\s*(No such user|\w+ (Not Found|file (was|has been) removed|no longer available)'
    TEMP_OFFLINE_PATTERN = r'>\s*\w+ server (is in )?(maintenance|maintainance)'


    def prepare(self):
        if not self.PLUGIN_DOMAIN:
            if self.account:
                account      = self.account
            else:
                account_name = (self.__name__ + ".py").replace("Folder.py", "").replace(".py", "")
                account      = self.pyload.accountManager.getAccountPlugin(account_name)

            if account and hasattr(account, "PLUGIN_DOMAIN") and account.PLUGIN_DOMAIN:
                self.PLUGIN_DOMAIN = account.PLUGIN_DOMAIN
            else:
                self.fail(_("Missing PLUGIN_DOMAIN"))

        if self.COOKIES:
            if isinstance(self.COOKIES, list) and (self.PLUGIN_DOMAIN, "lang", "english") not in self.COOKIES:
                self.COOKIES.insert((self.PLUGIN_DOMAIN, "lang", "english"))
            else:
                set_cookie(self.req.cj, self.PLUGIN_DOMAIN, "lang", "english")

        return super(XFSCrypter, self).prepare()
