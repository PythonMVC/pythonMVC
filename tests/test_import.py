"""Basic smoke tests for the PythonMVC package."""

import importlib


def test_package_loads_and_exports() -> None:
    package = importlib.import_module("PythonMVC")
    # minimal assurance the key APIs are exposed
    assert hasattr(package, "create_app")
    assert hasattr(package, "resource")
