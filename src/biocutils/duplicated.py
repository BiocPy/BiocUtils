import numpy


@singledispatch
def duplicated(x: Any, incomparables: set = set(), from_last: bool = False) -> numpy.ndarray:
    available = set()
    output = numpy.ndarray(len(x), dtype=numpy.bool_)

    def process(i, y):
        if y in incomparables:
            output[i] = False
        elif y in available:
            output[i] = True
        else:
            available.add(y)
            output[i] = False

    if not from_last:
        for i, y in enumerate(x):
            process(i, y)
    else:
        for i in range(len(x) - 1, -1, -1):
            process(i, x[i])

    return output


@duplicated.register
def _duplicated_Factor(x: Factor, incomparables: set = set(), from_last: bool = False) -> numpy.ndarray:
    present = []
    for lev in x.get_levels():
        if lev in incomparables:
            present.append(None)
        else:
            present.append(False)
    
    def process(i, y):
        tmp = present[i]
        if tmp is None:
            output[i] = False
        elif tmp:
            output[i] = True
        else:
            present[i] = True
            output[i] = False

    if not from_last:
        for i, y in enumerate(x):
            process(i, y)
    else:
        for i in range(len(x) - 1, -1, -1):
            process(i, x[i])

    return output


def unique(x: Any) -> Any:
    return subset(x, numpy.where(duplicated(x))[0])

