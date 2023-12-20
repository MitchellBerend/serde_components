# -*- coding: utf-8 -*-

# The test fixtures in this file are automagically imported to all test files

from typing import List
import pytest


class ConcreteRecord:
    def __init__(self, name=None, age=None):
        self.name = name
        self.age = age

    def __eq__(self, other) -> bool:
        return self.age == other.age and self.name == other.name

    def __repr__(self):
        return f"ConcreteRecord(name='{self.name}', age={self.age})"


@pytest.fixture
def record() -> ConcreteRecord:
    return ConcreteRecord(name='testName', age=10)


@pytest.fixture
def multiple_records() -> List[ConcreteRecord]:
    return [ConcreteRecord(name='testName', age=i) for i in range(10)]
