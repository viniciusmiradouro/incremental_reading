#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

import argparse


DEFAULTPATH = '/home/vm/brain'


parser = argparse.ArgumentParser(prog='ir')
parser.add_argument(
    'Path',
    nargs='?',
    default=DEFAULTPATH,
    help='Path of the directory containing elements'
)


arg_group = parser.add_mutually_exclusive_group(required=False)
arg_group.add_argument(
    '-R',
    '--reschedule',
    action='store_true',
    help="Reschedule elements in the collection"
)


args = parser.parse_args()
