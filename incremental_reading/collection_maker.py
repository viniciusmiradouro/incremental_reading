#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from datetime import date, datetime
from os import path, scandir

from mytypes import Collection, Element, File

asDate = datetime.fromtimestamp
modTime = path.getmtime


def iso2date(datestring: str) -> date:
    return datetime.fromisoformat(datestring).date()


def fileContents(file_path: str) -> File:
    with open(file_path, 'r', encoding='UTF-8') as file_lines:
        return tuple(file_lines)


def associatedElement(file_path: str, at_date: date = date.today()) -> Element:
    def attr(line: str) -> str:
        isolated_attr = line.split(': ')[1].strip()
        return isolated_attr

    file_contents = fileContents(file_path)
    priority = float(attr([i for i in file_contents if i.startswith('priority: ')][0]))
    reps = int(attr([i for i in file_contents if i.startswith('reps: ')][0]))
    review_date = iso2date(attr([i for i in file_contents if i.startswith('due_date: ')][0]))
    kind = attr([i for i in file_contents if i.startswith('kind: ')][0])
    name = next((i for i in file_contents if i.startswith('# ')))[2:].strip()
    was_modified = asDate(modTime(file_path)).date() == at_date

    try:
        return Element(name, file_path, was_modified, kind, priority, review_date, reps)
    except:
        print(f'failed to associate element to {file_path}. Exiting...')
        exit()


def associatedCollection(directory: str) -> Collection:
    def markdownFiles(directory: str) -> tuple[str, ...]:
        dir_files = tuple(map(lambda _: _.path, scandir(directory)))
        return tuple(i for i in dir_files if i.endswith('.md'))

    def validFiles(directory: str) -> tuple[str, ...]:
        return markdownFiles(directory)

    return Collection(map(associatedElement, validFiles(directory)))
