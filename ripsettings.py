import os
import configmanager

class RipSettings(dict):
    def __init__(self):
        self['audioformat'] = "flac"
        self['flacoptions'] = ["--best"]
        self['riplocation'] = os.environ['HOME'] + '/Music'
        self['tmpdir'] = '/tmp/riposte'
        self['filenameformat'] = '%a/%A/%n - %t'

    def initialize(self):
        cfg = configmanager.ConfigManager()
        settings = cfg.load_settings()
        cfgit = settings.iterkeys()

        while True:
            try:
                k = cfgit.next()
                if k in self:
                    self[k] = settings[k]
            except StopIteration:
                break
