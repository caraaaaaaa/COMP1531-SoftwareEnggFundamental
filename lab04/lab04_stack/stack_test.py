'''test class stack'''

from stack import Stack
import pytest

def test_push():
    '''test push method'''
    stack1 = Stack()
    stack1.push(4)
    assert stack1.stack == [4]

def test_pop():
    '''test pop method'''
    stack2 = Stack()
    stack2.push(4)
    stack2.pop()
    assert stack2.stack == []

def test_pop_empty():
    '''test pop from empty stack'''
    stack3 = Stack()
    with pytest.raises(ValueError):
        stack3.pop()
