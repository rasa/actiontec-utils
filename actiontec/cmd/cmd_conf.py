#!/usr/bin/python

import os
import sys
import argparse
import logging
import pprint

from .. import confparser

def handle_show(at, cfg, opts):
    parser = confparser.Parser()

    for path in opts.path:
        res, out = at.run('conf print %s' % path)
        if res != 0:
            logging.error('unable to show %s', path)
            continue

        fwcfg = parser.parse(out)
        pprint.pprint(fwcfg)

def handle_set(at, cfg, opts):
    if opts.prefix and not opts.prefix.endswith('/'):
        opts.prefix = opts.prefix + '/'

    i = iter(opts.nvpairs)
    for path, value in zip(i,i):
        logging.debug('set %s = %s', path, value)
        res, out = at.run('conf set %s%s %s' % (opts.prefix, path, value))
        if res != 0:
            logging.error('unable to set %s = %s', path, value)
            continue

def handle_del(at, cfg, opts):
    for path in opts.path:
        res, out = at.run('conf del %s' % path)
        if res != 0:
            logging.error('unable to delete %s', path)
            continue

def handle_commit(at, cfg, opts):
    res, out = at.run('conf reconf 1')
    print out
    return res

def add_parser(parent):
    parser = parent.add_parser('conf')
    sub = parser.add_subparsers()

    show_parser = sub.add_parser('show')
    show_parser.add_argument('path', nargs='+')
    show_parser.set_defaults(handler=handle_show)

    set_parser = sub.add_parser('set')
    set_parser.add_argument('--prefix', '-p', default='')
    set_parser.add_argument('nvpairs', nargs='+')
    set_parser.set_defaults(handler=handle_set)

    del_parser = sub.add_parser('del')
    del_parser.add_argument('path', nargs='+')
    del_parser.set_defaults(handler=handle_del)

    commit_parser = sub.add_parser('commit')
    commit_parser.set_defaults(handler=handle_commit)
