#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from datetime import date
from typing import NamedTuple


class Element(NamedTuple):
    name: str
    path: str
    acted_on: bool
    kind: str
    priority: float
    due_date: date
    reps: int


Collection = tuple[Element, ...]
File = tuple[str, ...]
Queue = tuple[str, ...]
