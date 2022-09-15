#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from datetime import date, timedelta
from typing import Optional
from type_declarations import Collection, Element


def check_is_due(element: Element):
    """
    Check if element is due today
    """
    if element['due'] > today():
        print("Element is not due today. Cannot execute repetition.")
        sys.exit()


def check_element_not_waiting(element: Element):
    """
    Check if element is not waiting for others
    """
    if element['waiting'] == [None]:
        print("Element is in wait. Cannot execute repetition.")
        sys.exit()


def check_valid_priority(priority: float):
    """
    Checks if provided priority is valid
    """
    try:
        assert 0 <= priority <= 1 and isinstance(
            priority, float), ("Priority must be a float between 0 and 1." +
                               " Changes Aborted.")
    except AssertionError as msg:
        print(msg)
        sys.exit()


def check_valid_path(path: Path):
    """
    Checks if provided path is valid
    """
    try:
        assert isinstance(path, Path), f"'{path}' is not a valid path."
    except AssertionError as msg:
        print(msg)
        sys.exit()


def check_valid_elements(col: Collection, elements: list[Optional[str]] = [None]):
    if elements:
        try:
            assert all(
                i in col.keys() for i in elements
            ), ("One of the elements is not a member of collection."
                + " Changes Aborted")
        except AssertionError as msg:
            print(msg)
            sys.exit()


def check_valid_element(col: Collection, element_id: str):
    """
    Check if element is in collection
    """
    try:
        assert element_id in col.keys(
        ), (f"'{element_id}' is not a member of collection. Changes Aborted.")
    except AssertionError as msg:
        print(msg)
        sys.exit()


def check_valid_status(status: str):
    """
    Check if provided status is valid for an element
    """
    try:
        assert status in [
            'Active', 'Inactive', 'Done'
        ], ("Status should be 'Active', 'Inactive' or 'Done'.",
            "Changes Aborted.")
    except AssertionError as msg:
        print(msg)
        sys.exit()


def check_valid_type(new_type: str):
    """
    Check if provided status is valid for an element
    """
    try:
        assert new_type in [
            'E', 'T', 'C'
        ], ("Status should be '(E)xtract', '(T)opic' or '(C)ontent'.",
            "Changes Aborted.")
    except AssertionError as msg:
        print(msg)
        sys.exit()


def today() -> date:
    """
    Returns todays date
    """
    return date.today()


def tomorrow() -> date:
    """
    Returns tomorrows date
    """
    return date.today() + timedelta(1)


def _get_max_id(col: Collection) -> int:
    """
    Returns the highest base 10 id from Collection
    """
    return max((int(_) for _ in col.keys()))


def gen_id(col: Collection) -> str:
    """
    Generates a sequential decimal id
    """
    last_id: int = _get_max_id(col)
    new_id: str = str(last_id + 1)
    padding: str = "0" * (5 - len(new_id))
    return padding + new_id
