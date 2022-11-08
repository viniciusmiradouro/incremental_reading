#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from datetime import date, timedelta

import helpers as h
from settings import (CONTENT_BASEINT, CONTENT_EASINESS, EXTRACT_BASEINT,
                      EXTRACT_EASINESS, MAXINT)
from type_declarations import Element


def schedule_postpone(element: Element) -> date:
    max_int = 21
    last_int = element['last_interval']
    priority = element['priority']
    eltype = element['type']
    params = [
        EXTRACT_BASEINT, CONTENT_BASEINT,
        MAXINT, CONTENT_EASINESS, EXTRACT_EASINESS
    ]
    assert all(i > 0 for i in params)
    if eltype == 'E':
        new_interval = (
            last_int / 2 * (EXTRACT_EASINESS + priority)
            if last_int / 2 >= EXTRACT_BASEINT
            else EXTRACT_BASEINT * (EXTRACT_EASINESS + priority)
        )
    else:
        new_interval = (
            last_int / 2 * (CONTENT_EASINESS + priority)
            if last_int / 2 >= CONTENT_BASEINT
            else CONTENT_BASEINT * (CONTENT_EASINESS + priority)
        )
    if new_interval <= max_int:
        return h.today() + timedelta(round(new_interval))
    return h.today() + timedelta(max_int)


def schedule_element(element: Element) -> Element:
    """
    Calculates schedule for a given element considering its previous
    interval, a constant base interval, easiness factor and max interval.
    (the last three are specified in settings.py)
    """

    params = [EXTRACT_BASEINT, CONTENT_BASEINT,
              MAXINT, CONTENT_EASINESS, EXTRACT_EASINESS]

    assert all(i > 0 for i in params)

    if element['type'] == 'E':
        new_interval = (
            element['last_interval'] * (
                EXTRACT_EASINESS + element['priority']
            )
            if element['last_interval'] >= EXTRACT_BASEINT
            else EXTRACT_BASEINT
        )

    else:
        new_interval = (
            element['last_interval'] * (
                CONTENT_EASINESS + element['priority']
            )
            if element['last_interval'] >= CONTENT_BASEINT
            else CONTENT_BASEINT
        )

    if new_interval > MAXINT:
        element['last_interval'] = MAXINT
        new_due: date = h.today() + timedelta(MAXINT)

    else:
        element['last_interval'] = new_interval
        new_due: date = h.today() + timedelta(round(new_interval))

    element['due'] = new_due
    element['rep_num'] += 1

    return element
