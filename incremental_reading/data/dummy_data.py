#!/usr/bin/env python
# -*- coding: utf-8 -*-

from type_declarations import Collection
from helpers import today

COLLECTION: Collection = {

    1: {
        'id': 1,
        'name': "How to Prove it",
        'consume_point': "p. 330",
        'parent_id': None,
        'type': "Topic",
        'due': today(),
        'last_interval': 0,
        'rep_num': 0,
        'priority': .15
    },

    2: {
        'id': 2,
        'name': "How to Prove it",
        'consume_point': "p. 330",
        'parent_id': None,
        'type': "Topic",
        'due': today(),
        'rep_num': 0,
        'last_interval': 0,
        'priority': .10
    },

    3: {
        'id': 3,
        'name': "How to Prove it",
        'consume_point': "p. 330",
        'parent_id': None,
        'type': "Topic",
        'due': today(),
        'last_interval': 0,
        'rep_num': 0,
        'priority': .20
    },

    4: {
        'id': 4,
        'name': "zk00358",
        'consume_point': "p. 330",
        'parent_id': None,
        'type': "Extract",
        'due': today(),
        'last_interval': 0,
        'rep_num': 0,
        'priority': .05
    },

}
