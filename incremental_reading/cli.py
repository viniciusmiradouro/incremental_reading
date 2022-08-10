#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from settings import DEFAULTPATH

# Init argument parser
parser = argparse.ArgumentParser(prog="ir")

# Required args
parser.add_argument("Path", nargs="?", default=DEFAULTPATH)

# Mutually exclusive group of optional args
arg_group = parser.add_mutually_exclusive_group(required=False)
arg_group.add_argument("-q", "--due_queue", nargs='?', type=int)
arg_group.add_argument("-r", "--execute_repetition", action='store', nargs="+")
arg_group.add_argument("-t", "--add_task", action='store', nargs="+")
arg_group.add_argument("-c", "--add_content", action='store', nargs="+")
arg_group.add_argument("-e", "--add_extract", action='store', nargs="+")
arg_group.add_argument("-l", "--list_collection", action='store_true')
arg_group.add_argument("-D", "--donify", action='store', type=str, nargs=1)
arg_group.add_argument("-rm", "--remove", action='store', type=str, nargs="+")
arg_group.add_argument("-W", "--change_dependence", action='store', nargs="+")
arg_group.add_argument("-s", "--change_status",
                       action='store', type=str, nargs=2)
arg_group.add_argument("-T", "--change_type",
                       action='store', type=str, nargs=2)
arg_group.add_argument("-P", "--change_priority",
                       action='store', nargs=2)

args = parser.parse_args()
