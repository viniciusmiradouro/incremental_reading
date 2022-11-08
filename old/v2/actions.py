#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from datetime import date

from functions import associatedCollection, dueQueue, updatedFiles


def reviewFiles(directory: str, ease_mod: float, due_date: date) -> None:

    def writeFile(file_name: str, content: tuple[str, ...]) -> None:
        with open(file_name, 'w', encoding='UTF-8') as out_file:
            for lines in content:
                out_file.write(lines)

    def writeReviewedFiles(updated_files: tuple[tuple[str, tuple[str, ...]], ...]) -> None:
        for _ in updated_files:
            writeFile(_[0], _[1])

    writeReviewedFiles(updatedFiles(directory, ease_mod, due_date))


def outputQueue(directory: str, due_date: date) -> None:
    print(dueQueue(associatedCollection(directory), due_date), end='')
