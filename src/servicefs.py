#!/usr/bin/env python

import logging
import yaml

from argparse import ArgumentParser
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn


class ServiceFS(LoggingMixIn, Operations):
    def __init__(self, cfg_path):
        with open(cfg_path) as cfgfile:
            self.cfg = yaml.load(cfgfile)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-c', '--configfile', dest='config_path', default='./servicefs.yml', help='Path to configuration file')
    parser.add_argument('mountpoint', help='Mount point')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    fuse = FUSE(ServiceFS(args.config_path), args.mountpoint, foreground=True)
