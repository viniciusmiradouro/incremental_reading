#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import secrets as s
from pathlib import Path
from datetime import date, timedelta
from typing import Optional
from type_declarations import Collection


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


def gen_id(col: Collection, size: int = 5) -> str:
    """
    Generates a random string based on the defined lexicon
    """
    lexicon = ("1234567890"
               + "abcdefghijklmnopqrstuvwxyz"
               + "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    item_id: str = "".join([s.choice(lexicon) for _ in range(size)])
    return (item_id if item_id not in col else gen_id(col))
