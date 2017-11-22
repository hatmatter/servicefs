#!/usr/bin/env python

from argparse import ArgumentParser
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-c', '--configfile', dest='config_path', default='./servicefs.yml', help='Path to configuration file')
    parser.add_argument('mountpoint', help='Mount point')
    args = parser.parse_args()

    fuse = FUSE()
