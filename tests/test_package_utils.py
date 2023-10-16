from biocutils.package_utils import is_package_installed

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_for_pandas():
    pkg = is_package_installed("pandas")

    assert pkg is False


def test_for_scipy():
    pkg = is_package_installed("scipy")

    assert pkg is False

def test_for_numpy():
    pkg = is_package_installed("numpy")

    assert pkg is True