#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
from typing import Optional
from pathlib import Path
from scheduler import schedule_element
from helpers import gen_id, today, tomorrow
from helpers import check_valid_elements, check_valid_status
from helpers import check_valid_path, check_valid_element, check_valid_priority
from type_declarations import Element, Queue, Collection


# IO to Collections
def create_collection(path: Path) -> None:
    """
    Creates a Collection at path
    """
    check_valid_path(path)
    with open(path, "xb") as file:
        pickle.dump({}, file)


def load_collection(path: Path) -> Collection:
    """
    Loads a Collection located at path
    """
    check_valid_path(path)
    if path.is_file():
        with open(path, "rb") as file:
            col: Collection = pickle.load(file)
        return col
    create_collection(path)
    return load_collection(path)


def save_collection(col: Collection, path: Path) -> None:
    """
    Saves a Collection at path
    """
    check_valid_path(path)
    with open(path, "wb") as file:
        pickle.dump(col, file)


# Adding topics
def _mk_content(col: Collection, name: str,
                consume_point: str, priority: float,
                waiting: list[Optional[str]] = [None]) -> Element:
    """
    Builds a topic entry for a given collection
    """
    topic: Element = {
        'id': gen_id(col), 'name': name,
        'consume_point': consume_point, 'parent_id': None,
        'type': 'C', 'due': today(), 'last_interval': 0,
        'rep_num': 0, 'status': 'Active', 'waiting': waiting,
        'priority': priority
    }
    return topic


def add_content(col: Collection, name: str, consume_point: str,
                priority: float, waiting: list[Optional[str]] = [None]) -> None:
    """
    Adds a new topic to a given collection with its respective:

    name, consume point, priority, waiting for element id
    """
    check_valid_priority(priority)
    check_valid_elements(col, waiting)
    new_topic: Element = _mk_content(
        col, name, consume_point, float(priority), waiting)
    col |= {new_topic['id']: new_topic}
    print(
        f"Topic [{new_topic['id']}] '{new_topic['name']}' added to collection.")


# Adding extracts
def _mk_extract(col: Collection, parent_id: str,
                name: str) -> Element:
    """
    Builds a extract entry for a given collection
    """
    parent_priority: float = col[parent_id]['priority']
    extract: Element = {
        'id': gen_id(col), 'name': name,
        'consume_point': None, 'parent_id': parent_id,
        'type': "E", 'due': tomorrow(), 'last_interval': 1,
        'rep_num': 0, 'status': 'Active', 'waiting': [],
        'priority': parent_priority
    }
    return extract


def add_extract(col: Collection, parent_id: str,
                name: str) -> None:
    """
    Adds a new extract from a topic of a given collection
    """
    check_valid_element(col, parent_id)
    new_extract: Element = _mk_extract(col, parent_id, name)
    col |= {new_extract['id']: new_extract}
    print(
        f"Extract [{new_extract['id']}] '{new_extract['name']}' added to collection.")


# Adding tasks
def _mk_task(col: Collection, name: str, priority: float) -> Element:
    """
    Builds a task entry for a given collection
    """
    extract: Element = {
        'id': gen_id(col), 'name': name,
        'consume_point': 'Do', 'parent_id': None,
        'type': "T", 'due': today(), 'last_interval': 0,
        'rep_num': 0, 'status': 'Active', 'waiting': [None],
        'priority': priority}
    return extract


def add_task(col: Collection, name: str, priority: float) -> None:
    """
    Adds new task to queue
    """
    check_valid_priority(priority)
    new_task: Element = _mk_task(col, name, priority)
    col |= {new_task['id']: new_task}
    print(
        f"Extract [{new_task['id']}] '{new_task['name']}' added to collection.")


# Print Due Queue
def _gather_due(col: Collection) -> Queue:
    """
    Selects elements from collection which are due today
    """
    due_elements: Queue = [col[element] for element in col if (
        col[element]['due'] <= today()
        and col[element]['status'] == 'Active'
        and col[element]['waiting'] == [None])]
    return due_elements


def _sort_due(queue: Queue) -> Queue:
    """
    Sorts a Queue of elements by their priority from lowest to highest and
    after their type from extracts to topics
    """
    order = {'T': 0, 'E': 1, 'C': 2}
    return sorted(queue, key=lambda element: (element['priority'],
                                              order[element['type']]))


def _gather_and_sort_due(col: Collection) -> Queue:
    """
    Composition of previous two functions
    """
    return _sort_due(_gather_due(col))


def list_due(col: Collection, stop: Optional[int] = None) -> None:
    """
    Prints the nth first due items of the queue
    """
    for num, element in enumerate(_gather_and_sort_due(col)):
        print(f"[{element['id']}] {element['name']},",
              f"{element['consume_point']} ({element['type']})",
              f"rep: {element['rep_num']}")

        if stop and (num > stop - 2):
            break


def list_collection(col: Collection) -> None:
    """
    List all elements and their attributes
    """
    element: Element
    for element in col.values():
        key: object
        val: object
        for key, val in element.items():
            print(f"{val}", end=", " if key != 'priority' else "\n")


# Actions taken on Elements
def execute_repetition(col: Collection, element_id: str,
                       new_consume_point: Optional[str] = None) -> None:
    """
    Calculates next due date, (optionally) change consume point and increments
    review count of an element
    """
    check_valid_element(col, element_id)
    col[element_id] = schedule_element(col[element_id])
    if new_consume_point:
        col[element_id]['consume_point'] = new_consume_point


def donify_element(col: Collection, element_id: str) -> None:
    """
    Mark element as done and set the waiting value for all elements'
    waiting for element to None
    """
    check_valid_element(col, element_id)
    for key in col.keys():
        if element_id in col[key]['waiting']:
            index = col[key]['waiting'].index(element_id)
            del col[key]['waiting'][index]
            if col[key]['waiting'] == []:
                col[key]['waiting'] = [None]
    col[element_id]['status'] = 'Done'


def remove_element(col: Collection, element_id: str) -> None:
    """
    Deletes and element from collection
    """
    check_valid_element(col, element_id)
    out: str = (f"Deleted [{element_id}] '{col[element_id]['name']}'"
                + " from collection.")
    del col[element_id]
    print(out)


def change_status(col: Collection, element_id: str, new_status: str) -> None:
    """
    Changes the status of an element
    """
    check_valid_element(col, element_id)
    check_valid_status(new_status)
    col[element_id]['status'] = new_status
    print(
        f"Changed element [{element_id}] '{col[element_id]['name']}'"
        + "status to '{new_status}'")
