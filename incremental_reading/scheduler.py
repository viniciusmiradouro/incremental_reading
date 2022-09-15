#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, timedelta
import helpers as h
from type_declarations import Element
from settings import ABSBASEINTERVAL, EASINESS, ABSMAXINTERVAL


def _rel_max_interval(element: Element) -> int:
    """
    calculates max interval based on priority
    """
    return round(element['priority'] * ABSMAXINTERVAL)


def schedule_element(element: Element) -> Element:
    """
    Calculates schedule for a given element considering its previous interval,
    a constant base interval, easiness factor and max interval. (the last three
    are specified in settings.py)
    """

    assert (EASINESS >= 1 and ABSBASEINTERVAL > 0 and ABSMAXINTERVAL > 0)

    new_interval: float = (element['last_interval'] * EASINESS
                           if element['last_interval'] != 0
                           else ABSBASEINTERVAL)

    maxinterval = _rel_max_interval(element)

    if new_interval > maxinterval:
        new_due: date = h.today() + timedelta(maxinterval)
        element['last_interval'] = maxinterval

    else:
        new_due: date = h.today() + timedelta(new_interval)
        element['last_interval'] = new_interval

    element['due'] = new_due
    element['rep_num'] += 1

    return element
