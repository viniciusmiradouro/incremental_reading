#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: func to smoothen priority
# TODO: func change elements properties
# TODO: func add randomness to q
# TODO: func dependence chain adding

import sys
from pathlib import Path
from typing import Optional
from cli import args
from interface import add_task, change_status, list_collection, remove_element
from interface import list_due, save_collection, execute_repetition
from interface import load_collection, add_content, add_extract, donify_element
from type_declarations import Collection

PATH: Path = args.Path
COLLECTION: Collection = load_collection(PATH)


def adds() -> None:
    """
    Operations that add items to collections
    """
    changed: bool = False

    # Adds contents
    if args.add_content:
        name: str = args.add_content[0]
        consume_point: str = args.add_content[1]
        priority: float = float(args.add_content[2])
        waiting: list[Optional[str]]
        if len(args.add_content) > 3:
            waiting = args.add_content[3:]
        else:
            waiting = []
        add_content(COLLECTION, name, consume_point, priority, waiting)
        changed = True

    # Adds extracts
    elif args.add_extract:
        parent_id: str = args.add_extract[0]
        name: str = args.add_extract[1]
        add_extract(COLLECTION, parent_id, name)
        changed = True

    # Adds extracts
    elif args.add_task:
        name: str = args.add_task[0]
        priority: float = float(args.add_task[1])
        add_task(COLLECTION, name, priority)
        changed = True

    if changed:
        save_collection(COLLECTION, PATH)


def deletions() -> None:
    """
    Actions that delete items from collection
    """
    changed: bool = False

    # Delete Element from collection
    if args.remove:
        for element_id in args.remove:
            remove_element(COLLECTION, element_id)
        changed = True

    if changed:
        save_collection(COLLECTION, PATH)


def alterations() -> None:
    """
    Grouping code that alters collections
    """
    changed: bool = False

    # Executes repetitions on Elements
    if args.execute_repetition:
        new_consume_point: Optional[str]
        element_id: str = args.execute_repetition[0]
        if len(args.execute_repetition) > 1:
            new_consume_point = args.execute_repetition[1]
        else:
            new_consume_point = None
        execute_repetition(COLLECTION, element_id, new_consume_point)
        changed = True

    # Changes an element Status
    elif args.change_status:
        element_id: str = args.change_status[0]
        new_status: str = args.change_status[1]
        change_status(COLLECTION, element_id, new_status)
        changed = True

    # Marks Element as done
    elif args.donify:
        element_id: str = args.donify[0]
        donify_element(COLLECTION, element_id)
        changed = True

    if changed:
        save_collection(COLLECTION, PATH)


def outputs() -> None:
    """
    Groups actions that output info from collections
    """
    # Lists whole collection
    if args.list_collection:
        list_collection(COLLECTION)

    # Lists first 5 Elements due today
    elif args.due_queue:
        stop_at = args.due_queue
        list_due(COLLECTION, stop_at)


def main() -> None:
    """
    Runs fundamental functions of program
    """
    adds()
    deletions()
    alterations()
    outputs()
    # for i in COLLECTION.keys():
    #     if COLLECTION[i]['type'] == 'T':
    #         COLLECTION[i]['type'] = 'C'
    # save_collection(COLLECTION, PATH)


if __name__ == "__main__":
    main()
    sys.exit()
