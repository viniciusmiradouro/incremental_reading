#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, timedelta
from helpers import today
from type_declarations import Element
from settings import BASEINTERVAL, EASINESS, MAXINTERVAL


def schedule_element(element: Element) -> Element:
    """
    Calculates schedule for a given element considering its previous interval,
    a constant base interval, easiness factor and max interval. (the last three
    are specified in settings.py)
    """

    assert (EASINESS >= 1 and BASEINTERVAL > 0 and MAXINTERVAL > 0)

    new_interval: float = (element['last_interval'] * EASINESS
                           if element['last_interval'] != 0
                           else BASEINTERVAL)

    if new_interval > MAXINTERVAL:
        new_due: date = today() + timedelta(MAXINTERVAL)
        element['last_interval'] = MAXINTERVAL

    else:
        new_due: date = today() + timedelta(new_interval)
        element['last_interval'] = new_interval

    element['due'] = new_due
    element['rep_num'] += 1

    return element
