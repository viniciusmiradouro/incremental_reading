#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from typing import Optional

from cli import args
from interface import (add_content, add_extract, add_task, change_cousins,
                       change_dependece, change_name, change_priority,
                       change_status, change_type, donify_element,
                       execute_repetition, list_collection, list_due,
                       load_collection, postpone, remove_element,
                       save_collection)
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
        priority = float(args.add_extract[0])
        name: str = args.add_extract[1]
        add_extract(COLLECTION, priority, name)
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

        # Changes an element type
    elif args.change_type:
        element_id: str = args.change_type[0]
        new_type: str = args.change_type[1]
        change_type(COLLECTION, element_id, new_type)
        changed = True

        # Changes an element dependeces
    elif args.change_dependence:
        element_id: str = args.change_dependence[0]
        new_dependecy: list[Optional[str]] = args.change_dependence[1:]
        change_dependece(COLLECTION, element_id, new_dependecy)
        changed = True

        # Changes an element cousins
    elif args.change_cousins:
        element_id: str = args.change_cousins[0]
        new_cousins: list[Optional[str]] = args.change_cousins[1:]
        change_cousins(COLLECTION, element_id, new_cousins)
        changed = True

        # Changes an element priority
    elif args.change_priority:
        element_id: str = args.change_priority[0]
        new_priority: float = float(args.change_priority[1])
        change_priority(COLLECTION, element_id, new_priority)
        changed = True

        # Changes an element name
    elif args.rename:
        element_id: str = args.rename[0]
        new_name: str = args.rename[1]
        change_name(COLLECTION, element_id, new_name)
        changed = True

        # Marks Element as done
    elif args.donify:
        element_id: str = args.donify[0]
        donify_element(COLLECTION, element_id)
        changed = True

    elif args.postpone:
        postpone(COLLECTION)
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

    # Lists first n Elements due today
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
    sys.exit()


if __name__ == "__main__":
    main()
