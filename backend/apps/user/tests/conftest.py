import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        if "model" in item.name:
            item.add_marker(pytest.mark.model)
        if "structure" in item.name:
            item.add_marker(pytest.mark.structure)
        if "constraints" in item.name:
            item.add_marker(pytest.mark.constraints)
        if "functional" in item.name:
            item.add_marker(pytest.mark.functional)
