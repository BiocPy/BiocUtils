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
from .StringList import StringList
from .IntegerList import IntegerList
from .FloatList import FloatList
from .BooleanList import BooleanList
from .Names import Names
from .NamedList import NamedList

from .factorize import factorize
from .intersect import intersect
from .is_list_of_type import is_list_of_type
from .is_missing_scalar import is_missing_scalar
from .map_to_index import map_to_index
from .match import match
from .normalize_subscript import normalize_subscript, SubscriptTypes
from .print_truncated import print_truncated, print_truncated_dict, print_truncated_list
from .print_wrapped_table import create_floating_names, print_type, print_wrapped_table, truncate_strings
from .union import union

from .combine import combine
from .combine_rows import combine_rows
from .combine_columns import combine_columns
from .combine_sequences import combine_sequences

from .relaxed_combine_columns import relaxed_combine_columns
from .relaxed_combine_rows import relaxed_combine_rows

from .extract_row_names import extract_row_names
from .extract_column_names import extract_column_names

from .subset import subset
from .subset_rows import subset_rows
from .subset_sequence import subset_sequence

from .which import which

from .assign import assign
from .assign_rows import assign_rows
from .assign_sequence import assign_sequence

from .show_as_cell import show_as_cell
from .convert_to_dense import convert_to_dense

from .get_height import get_height
from .is_high_dimensional import is_high_dimensional

from .biocobject import BiocObject
from .table import table

from .duplicated import duplicated, unique
