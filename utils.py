def clear_file(filename):
    with open(filename, 'w'):
        pass


def my_sorted(iterable: list, *, key=lambda x: x, reverse=False):
    """
    Functie de sortare proprie cu aceeasi structura ca sorted()
    din Python
    """
    for i in range(len(iterable) - 1):
        for j in range(i + 1, len(iterable)):
            if reverse:
                if key(iterable[i]) < key(iterable[j]):
                    iterable[i], iterable[j] = iterable[j], iterable[i]
            elif key(iterable[i]) > key(iterable[j]):
                iterable[i], iterable[j] = iterable[j], iterable[i]

    return iterable
