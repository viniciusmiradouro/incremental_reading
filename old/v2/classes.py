#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from datetime import date
from typing import NamedTuple


class Element(NamedTuple):
    status: str
    reference_path: str
    due_date: date
    priority: float
    interval: float
    ease: float
    score: int
    name: str
    path: str


Collection = tuple[Element, ...]
