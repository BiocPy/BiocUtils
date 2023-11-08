import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .Factor import Factor
from .factorize import factorize
from .intersect import intersect
from .is_list_of_type import is_list_of_type
from .is_missing_scalar import is_missing_scalar
from .map_to_index import map_to_index
from .match import match
from .normalize_subscript import normalize_subscript
from .print_truncated import print_truncated, print_truncated_dict, print_truncated_list
from .print_wrapped_table import create_floating_names, print_type, print_wrapped_table, truncate_strings
from .subset import subset
from .union import union

from .combine import combine
from .combine_rows import combine_rows
from .combine_columns import combine_columns
from .combine_sequences import combine_sequences

from .convert_to_dense import convert_to_dense
