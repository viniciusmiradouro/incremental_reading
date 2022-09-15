#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
from random import randint, choice
from pathlib import Path
from typing import Any, Optional
from settings import CONTENT_PERCENTAGE
from scheduler import schedule_element
from type_declarations import Element, Queue, Collection
import helpers as h


# IO to Collections
def create_collection(path: Path) -> None:
    """
    Creates a Collection at path
    """
    h.check_valid_path(path)
    with open(path, "xb") as file:
        pickle.dump({}, file)


def load_collection(path: Path) -> Collection:
    """
    Loads a Collection located at path
    """
    h.check_valid_path(path)
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
    h.check_valid_path(path)
    with open(path, "wb") as file:
        pickle.dump(col, file)


# Adding topics
def _mk_content(col: Collection, name: str,
                consume_point: str, priority: float,
                waiting: list[Optional[str]] = []) -> Element:
    """
    Builds a topic entry for a given collection
    """
    if not waiting:
        waiting = [None]

    topic: Element = {
        'id': h.gen_id(col), 'name': name,
        'consume_point': consume_point, 'parent_id': None,
        'type': 'C', 'due': h.today(), 'last_interval': 0,
        'rep_num': 0, 'status': 'Active', 'waiting': waiting,
        'priority': priority, 'cousins': [None]
    }
    return topic


# Adding extracts
def _mk_extract(col: Collection, parent_id: str,
                name: str) -> Element:
    """
    Builds a extract entry for a given collection
    """
    parent_priority: float = col[parent_id]['priority']
    extract: Element = {
        'id': h.gen_id(col), 'name': name,
        'consume_point': "Process", 'parent_id': parent_id,
        'type': "E", 'due': h.tomorrow(), 'last_interval': 1,
        'rep_num': 0, 'status': 'Active', 'waiting': [None],
        'priority': parent_priority, 'cousins': [None]
    }
    return extract


def _mk_task(col: Collection, name: str, priority: float) -> Element:
    """
    Builds a task entry for a given collection
    """
    extract: Element = {
        'id': h.gen_id(col), 'name': name,
        'consume_point': 'Do', 'parent_id': None,
        'type': "T", 'due': h.today(), 'last_interval': 0,
        'rep_num': 0, 'status': 'Active', 'waiting': [None],
        'priority': priority,
        'cousins': [None]}
    return extract


def add_task(col: Collection, name: str, priority: float) -> None:
    """
    Adds new task to queue
    """
    h.check_valid_priority(priority)
    new_task: Element = _mk_task(col, name, priority)
    col |= {new_task['id']: new_task}
    print(f"(T) [{new_task['id']}]",
          f"{new_task['name']!r} added to collection.")


def add_content(col: Collection, name: str,
                consume_point: str, priority: float,
                waiting: list[Optional[str]] = [None]) -> None:
    """
    Adds a new topic to a given collection with its respective:

    name, consume point, priority, waiting for element id
    """
    h.check_valid_priority(priority)
    h.check_valid_elements(col, waiting)
    new_topic: Element = _mk_content(
        col, name, consume_point, float(priority), waiting)
    col |= {new_topic['id']: new_topic}
    print(f"(C) [{new_topic['id']}]",
          f"{new_topic['name']!r} added to collection.")


def add_extract(col: Collection, parent_id: str,
                name: str) -> None:
    """
    Adds a new extract from a topic of a given collection
    """
    h.check_valid_element(col, parent_id)
    new_extract: Element = _mk_extract(col, parent_id, name)
    col |= {new_extract['id']: new_extract}
    print(f"(E) [{new_extract['id']}]",
          f"{new_extract['name']!r} added to collection.")


# Print Due Queue
def _gather_due(col: Collection) -> Queue:
    """
    Selects elements from collection which are due today
    """
    due_elements: Queue = [col[element] for element in col if (
        col[element]['due'] <= h.today()
        and col[element]['status'] == 'Active'
        and col[element]['waiting'] == [None])]
    return due_elements


def _gather_elements(col: Collection) -> Queue:
    """
    Selects elements from collection which are due today
    """
    return [col[element] for element in col]


def _sort_due(queue: Queue) -> Queue:
    """
    Sorts a Queue of elements by their priority from lowest to highest and
    after their type from extracts to topics
    """
    order = {'T': 2, 'E': 0, 'C': 1}
    return sorted(queue, key=lambda element: (element['priority'],
                                              order[element['type']]))


def _sep_contents(queue: Queue) -> Queue:
    return [cont for cont in queue if cont['type'] in ['C', 'T']]


def _separate_extracts(queue: Queue) -> Queue:
    return [cont for cont in queue if cont['type'] == 'E']


def _remove(lst: list, element: Any):
    new_lst = lst.copy()
    new_lst.remove(element)
    return new_lst


def _pick(q: Queue, s: int, pr: int) -> Queue:
    """
    q := queue, s := size of output queue,
    pr := percentage of random picks, r := random integer.
    """
    q = _sort_due(q)

    def __pick(q: Queue, s: int, pr: int) -> Queue:
        r: int = randint(1, 100)
        return (
            [] if s == 0 else
            [q[0]] + __pick(q[1:], (s - 1), pr) if r > pr else
            [c := choice(q)] + __pick(_remove(q, c), (s - 1), pr)
        )

    return __pick(q, s, pr)


def _sep_by_type(col: Collection) -> tuple[Queue, Queue]:
    return (_sep_contents((due := _gather_due(col))), _separate_extracts(due))


def _build_schedule(col: Collection, size: int, rand_percent: int) -> Queue:
    amnt_con: int = round(size * CONTENT_PERCENTAGE)
    amnt_ext: int = size - amnt_con
    separator: tuple[Queue, Queue] = _sep_by_type(col)
    prepare = (_pick(separator[0], amnt_con, rand_percent)
               + _pick(separator[1], amnt_ext, rand_percent))
    return _pick(prepare, size, rand_percent)


def list_due(col: Collection, size: int, rand_percent: int) -> None:
    """
    Prints the nth first due items of the queue
    """
    for element in _build_schedule(col, size, rand_percent):
        print(
            f"[{element['id']}] {element['name']},",
            f"{element['consume_point']}, ({element['type']}),",
            f"rep: {element['rep_num']}"
            # , f"last interval: {element['last_interval']} "
        )


def list_collection(col: Collection) -> None:
    """
    List all elements and their attributes
    """
    for element in _gather_elements(col):
        for key, val in element.items():
            print(f"{val}", end="; " if key != 'cousins' else "\n")


# Actions taken on Elements
def execute_repetition(col: Collection, element_id: str,
                       new_consume_point: Optional[str] = None) -> None:
    """
    Calculates next due date, (optionally) change consume point and increments
    review count of an element
    """
    h.check_valid_element(col, element_id)
    h.check_is_due(col[element_id])
    col[element_id] = schedule_element(col[element_id])
    if new_consume_point:
        col[element_id]['consume_point'] = new_consume_point
    print(f"Rescheduled {col[element_id]['name']!r}.")


def donify_element(col: Collection, element_id: str) -> None:
    """
    Mark element as done and set the waiting value for all elements'
    waiting for element to None
    """
    h.check_valid_element(col, element_id)
    for key in col.keys():
        if element_id in col[key]['waiting']:
            index = col[key]['waiting'].index(element_id)
            del col[key]['waiting'][index]
            if col[key]['waiting'] == []:
                col[key]['waiting'] = [None]
    col[element_id]['status'] = 'Done'
    print(f"Marked {col[element_id]['name']!r} as done.")


def remove_element(col: Collection, element_id: str) -> None:
    """
    Deletes and element from collection
    """
    h.check_valid_element(col, element_id)
    out: str = (f"Deleted [{element_id}] '{col[element_id]['name']}'"
                + " from collection.")
    del col[element_id]
    print(out)


def change_status(col: Collection, element_id: str, new_status: str) -> None:
    """
    Changes the status of an element
    """
    h.check_valid_element(col, element_id)
    h.check_valid_status(new_status)
    col[element_id]['status'] = new_status
    print(f"Changed [{element_id}] {col[element_id]['name']!r}",
          f"status to {new_status!r}")


def change_type(col: Collection, element_id: str, new_type: str) -> None:
    """
    Changes element type
    """
    h.check_valid_element(col, element_id)
    h.check_valid_type(new_type)
    col[element_id]['type'] = new_type
    print(f"Changed [{element_id}]",
          f"{col[element_id]['name']!r} type to {new_type!r}")


def change_dependece(col: Collection, element_id: str,
                     new_dependency: list[Optional[str]]) -> None:
    """
    Changes element dependeces
    """
    h.check_valid_element(col, element_id)
    if new_dependency:
        for _id in new_dependency:
            if _id is not None:
                h.check_valid_element(col, _id)
        col[element_id]['waiting'] = new_dependency
    else:
        col[element_id]['waiting'] = [None]


def change_cousins(col: Collection, element_id: str,
                   new_cousins: list[Optional[str]]) -> None:
    """
    Changes element dependeces
    """
    h.check_valid_element(col, element_id)
    if new_cousins:
        for _id in new_cousins:
            if _id is not None:
                h.check_valid_element(col, _id)
        col[element_id]['cousins'] = new_cousins
    else:
        col[element_id]['cousins'] = [None]


def change_priority(col: Collection, element_id: str, new_priority: float):
    """
    Changes element priority
    """
    h.check_valid_element(col, element_id)
    h.check_valid_priority(new_priority)
    col[element_id]['priority'] = new_priority


def change_name(col: Collection, element_id: str, new_name: str):
    """
    Changes element name
    """
    h.check_valid_element(col, element_id)
    col[element_id]['name'] = new_name
    print(f"Changed [{element_id}]",
          f"{col[element_id]['name']!r} name to {new_name!r}")
