"""
Soft assertions — collect all failures in a test and report them together.

Usage:
    def test_example(soft):
        soft.assert_equal(actual, expected, "label")
        soft.assert_true(condition, "label")
        # All failures reported at end of test via the fixture teardown
"""
from __future__ import annotations

import pytest
from typing import Any


class SoftAssertions:
    def __init__(self) -> None:
        self._failures: list[str] = []

    def assert_equal(self, actual: Any, expected: Any, label: str = "") -> None:
        if actual != expected:
            msg = f"[{label}] Expected {expected!r}, got {actual!r}"
            self._failures.append(msg)

    def assert_true(self, condition: bool, label: str = "") -> None:
        if not condition:
            self._failures.append(f"[{label}] Expected True, got False")

    def assert_false(self, condition: bool, label: str = "") -> None:
        if condition:
            self._failures.append(f"[{label}] Expected False, got True")

    def assert_in(self, member: Any, container: Any, label: str = "") -> None:
        if member not in container:
            self._failures.append(f"[{label}] {member!r} not found in {container!r}")

    def assert_all(self) -> None:
        if self._failures:
            failure_report = "\n".join(f"  {i + 1}. {f}" for i, f in enumerate(self._failures))
            pytest.fail(f"Soft assertion failures:\n{failure_report}")


@pytest.fixture()
def soft() -> SoftAssertions:
    """Pytest fixture that yields a SoftAssertions instance and auto-asserts at teardown."""
    sa = SoftAssertions()
    yield sa
    sa.assert_all()
