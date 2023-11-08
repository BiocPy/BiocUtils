def _check_array_dimensions(x, active: int) -> bool:
    first = x[0].shape
    for i in range(1, len(x)):
        current = x[i].shape
        if len(first) != len(current):
            raise ValueError("inconsistent dimensions for combining arrays (expected " + str(len(first)) + ", got " + str(len(current)) + " for array " + str(i) + ")")
        for j in range(len(first)):
            if j != active and first[j] != current[j]:
                raise ValueError("inconsistent dimension extents for combining arrays on dimension " + str(active) + " (expected " + str(first[active]) + ", got " + str(current[active]) + " for array " + str(i) + ")")


def _coerce_sparse_matrix(first, combined, module):
    if isinstance(first, module.csr_matrix):
        return combined.tocsr()
    elif isinstance(first, module.csc_matrix):
        return combined.tocsc()
    elif isinstance(first, module.bsr_matrix):
        return combined.tobsr()
    elif isinstance(first, module.coo_matrix):
        return combined.tocoo()
    elif isinstance(first, module.dia_matrix):
        return combined.todia()
    elif isinstance(first, module.lil_matrix):
        return combined.tolil()
    else:
        return combined


def _coerce_sparse_array(first, combined, module):
    if isinstance(first, module.csr_array):
        return combined.tocsr()
    elif isinstance(first, module.csc_array):
        return combined.tocsc()
    elif isinstance(first, module.bsr_array):
        return combined.tobsr()
    elif isinstance(first, module.coo_array):
        return combined.tocoo()
    elif isinstance(first, module.dia_array):
        return combined.todia()
    elif isinstance(first, module.lil_array):
        return combined.tolil()
    else:
        return combined
