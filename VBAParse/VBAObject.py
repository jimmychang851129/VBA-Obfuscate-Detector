#!/usr/bin/env python

class VBAObject():
    def __init__(self, ioc, rev_codes=None, src_codes=None):
        self.ioc = ioc
        self.rev_codes = rev_codes # Should be a dic {stream: []}
        self.src_codes = src_codes # Should be a dic {stream: []}

    @property
    def rev_codes(self):
        return self._rev_codes

    @property
    def src_codes(self):
        return self._src_codes

    @rev_codes.setter
    def rev_codes(self, new_codes):
        self._rev_codes = new_codes

    @src_codes.setter
    def src_codes(self, new_codes):
        self._src_codes = new_codes
        