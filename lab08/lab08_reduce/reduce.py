def reduce(f, xs):
    if len(xs) == 0:
        return None
    else:
        result = xs[0]
        for element in xs[1:]:
            result = f(result, element)
        return result

if __name__ == '__main__': # pragma: no cover
    print(reduce(lambda x, y: x + y, [1,2,3,4,5]))
    print(reduce(lambda x, y: x * y, [1,2,3,4,5]))
