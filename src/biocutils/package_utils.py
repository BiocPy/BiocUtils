__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def is_package_installed(package_name: str) -> bool:
    """Check if the package is installed.

    Args:
        package_name (str): Package name.

    Returns:
        bool: True if package is installed, otherwise False.
    """
    _installed = False
    try:
        exec(f"import {package_name}")
        _installed = True
    except Exception:
        pass

    return _installed
