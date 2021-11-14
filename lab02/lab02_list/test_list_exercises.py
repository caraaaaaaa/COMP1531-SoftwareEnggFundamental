from list_exercises import *

def test_reverse():
    l = ["how", "are", "you"]
    l2 = [1, 2, 3, 4]
    l3 = []
    l4 = ["Cara"]
    l5 = [77]
    reverse_list(l)
    reverse_list(l2)
    reverse_list(l3)
    reverse_list(l4)
    reverse_list(l5)
    assert l == ["you", "are", "how"]
    assert l2 == [4, 3, 2, 1]
    assert l3 == []
    assert l4 == ["Cara"]
    assert l5 == [77]

def test_min_positive():
    assert minimum([1, 2, 3, 10]) == 1
    assert minimum([1]) == 1
    assert minimum([-1, 0, 2]) == -1
    assert minimum(["a", "b"]) == "a"

def test_sum_positive():
    assert sum_list([7, 7, 7]) == 21
    assert sum_list([]) == 0
    assert sum_list([1]) == 1
