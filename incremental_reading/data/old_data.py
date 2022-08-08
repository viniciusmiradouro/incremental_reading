#!/usr/bin/env python
# -*- coding: utf-8 -*-

Id = int
Priority = int
ChildOf = Id
ContentName = str
ConsumePoint = str
ContentType = str
Item = tuple[Id, ChildOf,  ContentName, ConsumePoint, ContentType, Priority]
Stack = tuple[Item, ...]
Collection = tuple[Stack, ...]

PRIMARY: Stack = (
)

SECONDARY: Stack = (
    (5, 3, 'zk00490', 'process', 'extract', 1),
    (6, 3, 'zk00491', 'process', 'extract', 1),
    (10, 3, 'zk00495', 'process', 'extract', 1),
    (12, 3, 'zk00497', 'process', 'extract', 1),
    (22, 19, 'zk00488', 'ankifi', 'extract', 1),
    (23, 19, 'zk00503', 'process', 'extract', 1),
    (24, 19, 'zk00504', 'process', 'extract', 1),
    (25, 19, 'zk00505', 'process', 'extract', 1),
    (26, 19, 'zk00506', 'process', 'extract', 1),

    (27, 27, 'Beyond the Basic Stuff', 'p. 86', 'book', 1),
    (28, 28, 'Python one liners', 'p. 3', 'to process book', 1),
    (31, 31, 'Hubermann Memory', '00m', 'podcast', 1),
)

TERTIARY: Stack = (
    (30, 30, 'Category Theory a Gentle intro', 'p. 1', 'book', -1),

    (32, 32, 'Speed Reading smemo', '0%m', 'webpage', 1),
    (33, 33, 'Hubermann Workspace', '00m', 'podcast', 1),
    (34, 34, 'Como ler um texto filosófico', '11', 'book', 1),
    (35, 35, 'Gwern spaced repetition', '0%', 'webpage', 1),
    (36, 36, 'Gramática do português contemporâneo', 'p. 1', 'book', 1),
    (37, 37, 'Behavioral models of impulsivity in ADHD', 'p. 1', 'paper', 1),
    (38, 38, 'How the amount and spacing...', 'p. 5(2)', 'paper', 1),
    (39, 39, 'Talento e Superdotação', 'p. 1', 'book', 1),
    (40, 38, 'zk00490', 'process', 'extract', 1),
    (41, 38, 'zk00518', 'process', 'extract', 1),
    (42, 38, 'zk00519', 'process', 'extract', 1),
    (43, 38, 'zk00520', 'process', 'extract', 1),
    (44, 38, 'zk00521', 'process', 'extract', 1),
    (45, 38, 'zk00522', 'process', 'extract', 1),
)
