#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from datetime import date, timedelta
from typing import Any

from collection_maker import fileContents
from mytypes import Collection, Element
from queue_maker import dueCollection, orderedCollection

Pair = tuple[Any, Any]
Pairs = tuple[Pair, ...]


def rescheduledElement(element: Element, review_date: date) -> Element:
    def nextReview(element: Element, review_date: date) -> date:
        if element.kind == 'Note':
            return review_date + timedelta(2 * (1.5 + element.priority)**element.reps)
        return review_date + timedelta(4 * (1.2 + element.priority)**element.reps)

    return Element(
        element.name,
        element.path,
        False,
        element.kind,
        element.priority,
        nextReview(element, review_date),
        element.reps + 1
    )


def postponedElement(element: Element, review_date: date) -> Element:
    def postponeReview(element: Element, review_date: date) -> date:
        if element.kind == 'Note':
            return review_date + timedelta(1 * (1.5 + element.priority)**element.reps)
        return review_date + timedelta(2 * (1.2 + element.priority)**element.reps)

    return Element(
        element.name,
        element.path,
        False,
        element.kind,
        element.priority,
        postponeReview(element, review_date),
        element.reps
    )


def scheduleElementTomorrow(element: Element, review_date: date) -> Element:
    return Element(
        element.name,
        element.path,
        False,
        element.kind,
        element.priority,
        review_date + timedelta(1),
        element.reps
    )


def rescheduledElements(collection: Collection, review_date: date) -> Collection:
    def partitionEdited(collection: Collection, review_date: date) -> tuple[Collection, ...]:
        due_collection = dueCollection(collection, review_date)
        unedited = orderedCollection(Collection(filter(lambda _: not(_.acted_on), due_collection)))
        reschedule = Collection(filter(lambda _: _.acted_on, due_collection))
        skip = unedited[:round(len(due_collection) * .20)]
        postpone = unedited[round(len(due_collection) * .20):]
        return reschedule, skip, postpone

    to_update = partitionEdited(collection, review_date)

    rescheduled = Collection(map(lambda _: rescheduledElement(_, review_date), to_update[0]))
    skiped = Collection(map(lambda _: scheduleElementTomorrow(_, review_date), to_update[1]))
    postponed = Collection(map(lambda _: postponedElement(_, review_date), to_update[2]))

    return rescheduled + skiped + postponed


def withUpdatedFooter(element: Element) -> Pair:
    file_body = fileContents(element.path)[:-6]
    footer = (
        '---\n',
        f'due_date: {element.due_date}\n',
        f'priority: {element.priority}\n',
        f'reps: {element.reps}\n',
        f'kind: {element.kind}\n',
        '---'
    )
    updated_file = file_body + footer
    return (element.path, updated_file)


def updatedFiles(collection: Collection, review_date: date) -> Pairs:
    reviewed = rescheduledElements(collection, review_date)
    return tuple(map(withUpdatedFooter, reviewed))
