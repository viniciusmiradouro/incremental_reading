#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from datetime import date

from mytypes import Collection, Queue

def dueCollection(collection: Collection, due_date: date) -> Collection:
    due_elements = filter(lambda _: _.due_date < due_date, collection)
    return Collection(due_elements)


def orderedCollection(collection: Collection) -> Collection:
    return Collection(sorted(collection, key=lambda _: _.priority))


def dueQ(collection: Collection, due_date: date, size: int) -> str:
    def partition(collection: Collection) -> tuple[Collection, Collection]:
        notes = Collection(filter(lambda _: _.kind == 'Note', collection))
        others = Collection(filter(lambda _: _.kind != 'Note', collection))
        return orderedCollection(notes), orderedCollection(others)

    def finalQ(collection: Collection) -> Collection:
        notes, others = partition(dueCollection(collection, due_date))
        amnt_notes = round(size * .85)
        return orderedCollection(others[:size - amnt_notes] + notes[:amnt_notes])

    return "\n".join(Queue(map(lambda _: f'[[{_.name}]]', finalQ(collection))))
