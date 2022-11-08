#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

from datetime import date

from queue_maker import dueQ
from scheduler import updatedFiles
from collection_maker import associatedCollection
from mytypes import File


def reviewFiles(directory: str, due_date: date) -> None:

    def writeFile(file_path: str, content: File) -> None:
        with open(file_path, 'w', encoding='UTF-8') as out_file:
            for lines in content:
                out_file.write(lines)

    def writeReviewedFiles(updated_files: tuple[tuple[str, File], ...]) -> None:
        for _ in updated_files:
            path = _[0]
            content = _[1]
            writeFile(path, content)

    collection = associatedCollection(directory)

    writeReviewedFiles(updatedFiles(collection, due_date))


def outputQueue(directory: str, due_date: date, size: int) -> None:
    collection = associatedCollection(directory)
    print(dueQ(collection, due_date, size))
