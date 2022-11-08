#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from datetime import date

from actions import outputQueue, reviewFiles
from cli import args


def main() -> None:
    if args.reschedule:
        reviewFiles(args.Path, .2, date.today())
    else:
        outputQueue(args.Path, date.today())


if __name__ == '__main__':
    main()
