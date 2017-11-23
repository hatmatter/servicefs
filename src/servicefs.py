#!/usr/bin/env python

import logging
import yaml

from argparse import ArgumentParser
from errno import ENOENT
from stat import S_IFDIR, S_IFREG
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from time import time


class Namespace():
    def __init__(self, name, children=None):
        now = time()
        self.name = name
        self.children = children or {}
        self.attr = dict(st_mode=(S_IFDIR | 0o755),
                         st_ctime=now,
                         st_mtime=now,
                         st_atime=now,
                         st_nlink=2)

    def __repr__(self):
        s = '<NS>:{}'.format(self.name)
        for c in self.children.values():
            s += '\n{}'.format(c)
        return s


class Plugin():
    def __init__(self, name, plugin_name, **plugin_args):
        import os
        base = os.path.dirname(os.path.realpath(__file__))
        plugin_path = base+'/plugins/'+plugin_name.lower()+'.py'

        import importlib.util
        spec = importlib.util.spec_from_file_location('aplugin', plugin_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.plugin = getattr(mod, plugin_name)(**plugin_args)
        self.name = name

    def __repr__(self):
        return '<Plugin|{}>:{}'.format(self.plugin.__class__.__name__, self.name)



class ServiceFS(LoggingMixIn, Operations):
    def __init__(self, cfg_path):
        with open(cfg_path) as cfgfile:
            self.cfg = yaml.load(cfgfile)

        self.root = self._create_tree('/', self.cfg['layout'])
        print(self.root)


    def _load_plugin(self, name):
        import os
        base = os.path.dirname(os.path.realpath(__file__))
        plugin_path = base+'/plugins/'+name.lower()+'.py'

        import importlib.util
        spec = importlib.util.spec_from_file_location('aplugin', plugin_path)
        plugin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin)
        return getattr(plugin, name)


    def _create_tree(self, name, root):
        children = {}
        for k,v in root.items():
            if v is None:
                children[k] = Namespace(k)
            else:
                if '_plugin_' in v:
                    children[k] = Plugin(k, v['_plugin_'], **v)
                else:
                    children[k] = self._create_tree(k, v)
        return Namespace(name, children)


    ##########################
    # FUSE functions
    ##########################

    def readdir(self, path, fh):
        keys = path.split('/')
        cdir = self.tree
        for entry in [_ for _ in path.split('/') if _ != '']:
            if entry in cdir:
                cdir = cdir[entry]
            else:
                raise FuseOSError(ENOENT)
        return ['.', '..'] + list(cdir.keys())


    def getattr(self, path, fh=None):
        pass


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-c', '--configfile',
                        dest='config_path',
                        default='./servicefs.yml',
                        help='Path to configuration file')
    parser.add_argument('mountpoint', help='Mount point')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    fuse = FUSE(ServiceFS(args.config_path), args.mountpoint, foreground=True)
