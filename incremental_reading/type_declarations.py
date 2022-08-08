#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
from typing import Optional, TypedDict

Element = TypedDict('Element', {'id': str, 'name': str, 'consume_point':
                                Optional[str], 'parent_id': Optional[str],
                                'type': str, 'due': date, 'last_interval':
                                float, 'rep_num': int, 'status': str,
                                'waiting': list[Optional[str]], 'priority': float})
Collection = dict[str, Element]
Queue = list[Element]
