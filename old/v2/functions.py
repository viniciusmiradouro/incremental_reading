#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from datetime import date, timedelta
from os import scandir
from typing import Any
from functools import lru_cache

from classes import Collection, Element
from dateutil.parser import parse
from toolz import apply

Queue = File = tuple[str, ...]
Pair = tuple[Any, Any]
Pairs = tuple[Pair, ...]


def fileContents(file: str) -> File:
    with open(file, 'r', encoding='UTF-8') as file_lines:
        return tuple(file_lines)


def newEase(element: Element, ease_mod: float) -> float:
    @lru_cache(64)
    def _newEase(ease: float, ease_mod: float, score: int) -> float:
        return ease + (ease_mod * score)
    return _newEase(element.ease, ease_mod, element.score)


def newInterval(element: Element, ease_mod: float) -> float:
    @lru_cache(64)
    def _newInterval(interval: float, ease: float, ease_mod: float, score: int) -> float:
        return interval * ease * (1 + ease_mod * score)
    return _newInterval(element.interval, element.ease, ease_mod, element.score)


def newDueDate(element: Element, ease_mod: float, reviewed: date) -> date:
    return reviewed + timedelta(newInterval(element, ease_mod))


def rescheduledElement(element: Element, ease_mod: float, reviewed: date) -> Element:
    attributes = (
        element.status,
        element.reference_path,
        newDueDate(element, ease_mod, reviewed),
        element.priority,
        newInterval(element, ease_mod),
        newEase(element, ease_mod),
        0,
        element.name,
        element.path
    )
    return Element(*attributes)


def attributeInLine(line: str) -> str:
    return line.split(': ')[1].strip()


def fileAttributes(file: str) -> File:
    return File(map(attributeInLine, fileContents(file)[-10:-1]))


def asDate(date_string: str) -> date:
    return parse(date_string).date()


def associatedElement(file: str) -> Element:
    conversions = (str, str, asDate, float, float, float, int, str, str)
    return Element(*tuple(map(apply, conversions, fileAttributes(file))))


def markdownFiles(directory: str) -> File:
    dir_files = map(lambda _: _.path, scandir(directory))
    return tuple(filter(lambda file: file.endswith('.md'), dir_files))


def validFiles(directory: str) -> File:
    return markdownFiles(directory)


def associatedCollection(directory: str) -> Collection:
    return Collection(map(associatedElement, validFiles(directory)))


def isDue(element: Element, at_date: date) -> bool:
    return element.due_date < at_date


def dueElements(collection: Collection, due_date: date) -> Collection:
    return Collection(filter(lambda _: isDue(_, due_date), collection))


def orderByPriority(collection: Collection) -> Collection:
    return Collection(sorted(collection, key=lambda _: _.priority))


def ordQueue(collection: Collection, due_date: date) -> Collection:
    return orderByPriority(dueElements(collection, due_date))


def reviewedElements(collection: Collection, ease_mod: float, reviewed: date) -> Collection:
    newSchedule = lambda _: rescheduledElement(_, ease_mod, reviewed)
    return Collection(map(newSchedule, dueElements(collection, reviewed)))


def withUpdatedFooter(element: Element) -> Pair:
    file_body = fileContents(element.path)[:-11]
    footer = (
        '---\n',
        f'status: {element.status}\n',
        f'reference_path: {element.reference_path}\n',
        f'due_date: {element.due_date}\n',
        f'priority: {element.priority}\n',
        f'interval: {element.interval}\n',
        f'ease: {element.ease}\n',
        f'score: {element.score}\n',
        f'name: {element.name}\n',
        f'path: {element.path}\n',
        '---'
    )
    updated_file = file_body + footer
    return (element.path, updated_file)


def dueQueue(collection: Collection, due_date: date) -> str:
    name = lambda _: '[[' + _.name + ']]'
    return "\n".join(Queue(map(name, ordQueue(collection, due_date))))


def updatedFiles(directory: str, ease_mod: float, due: date) -> Pairs:
    collection = associatedCollection(directory)
    reviewed = reviewedElements(collection, ease_mod, due)
    return tuple(map(withUpdatedFooter, reviewed))
