from biocutils.package_utils import is_package_installed

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

def test_installed_package():
    assert is_package_installed("scipy")
    assert is_package_installed("numpy")
    assert not is_package_installed("some_random_package")
