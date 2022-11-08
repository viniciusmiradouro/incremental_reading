#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from datetime import date, datetime
from os import path, scandir

from mytypes import Collection, Element, File


def fileContents(file_path: str) -> File:
    with open(file_path, 'r', encoding='UTF-8') as file_lines:
        return tuple(file_lines)


def associatedElement(file_path: str) -> Element:

    def wasModified(file_path: str) -> bool:  # impure
        asDate = datetime.fromtimestamp
        modTime = path.getmtime
        today = date.today()
        return asDate(modTime(file_path)).date() == today

    def isolateAttr(line: str) -> str:
        return line.split(': ')[1].strip()

    def name(contents: File) -> str:
        name_line = next((i for i in contents if i.startswith('# ')))
        return name_line[2:].strip()

    def dueDate(contents: File) -> date:
        date_line = next((i for i in contents if i.startswith('due_date: ')))
        return datetime.fromisoformat(isolateAttr(date_line)).date()

    def kind(contents: File) -> str:
        kind_line = next((i for i in contents if i.startswith('kind: ')))
        return isolateAttr(kind_line)

    def priority(contents: File) -> float:
        priority_line = next((i for i in contents if i.startswith('priority: ')))
        return float(isolateAttr(priority_line))

    def repetitions(contents: File) -> int:
        reps_line = next(i for i in contents if i.startswith('reps: '))
        return int(isolateAttr(reps_line))

    file_contents = fileContents(file_path)

    try:
        return Element(
            name(file_contents),
            file_path,
            wasModified(file_path),
            kind(file_contents),
            priority(file_contents),
            dueDate(file_contents),
            repetitions(file_contents)
        )
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
