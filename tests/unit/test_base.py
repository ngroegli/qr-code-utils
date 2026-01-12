"""
Base classes and utilities for unit tests.
"""
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod


class TestResult:
    """Represents a single test result."""

    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.message = ""
        self.details = {}

    def set_passed(self, message: str = "Test passed"):
        """Mark the test as passed."""
        self.passed = True
        self.message = message

    def set_failed(self, message: str = "Test failed"):
        """Mark the test as failed."""
        self.passed = False
        self.message = message

    def add_detail(self, key: str, value: Any):
        """Add a detail to the test result."""
        self.details[key] = value

    def __str__(self):
        """String representation of the test result."""
        status = "PASS" if self.passed else "FAIL"

        # ANSI color codes
        green = "\033[92m"
        red = "\033[91m"
        reset = "\033[0m"

        # Color the status
        if self.passed:
            colored_status = f"{green}{status}{reset}"
        else:
            colored_status = f"{red}{status}{reset}"

        result_str = f"{self.name}: {colored_status} - {self.message}"

        # Add details if present
        if self.details:
            result_str += "\n  Details:"
            for key, value in self.details.items():
                result_str += f"\n    {key}: {value}"

        return result_str


class BaseUnitTest(ABC):
    """Base class for all unit tests."""

    def __init__(self):
        self.name = self.__class__.__name__
        self.results = []

    @abstractmethod
    def run(self) -> List[TestResult]:
        """Run the test and return results."""

    def add_result(
        self,
        test_name: str,
        passed: bool,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """Add a test result."""
        result = TestResult(test_name)
        if passed:
            result.set_passed(message)
        else:
            result.set_failed(message)

        if details:
            for key, value in details.items():
                result.add_detail(key, value)

        self.results.append(result)
        return result

    def assert_equal(self, expected, actual, test_name: str, message: str = ""):
        """Assert that expected equals actual."""
        passed = expected == actual
        details = {
            "expected": expected,
            "actual": actual,
        }
        full_message = message or "Values are equal"
        if not passed:
            full_message = f"{message} - Expected {expected}, got {actual}"
        return self.add_result(test_name, passed, full_message, details)

    def assert_not_equal(self, not_expected, actual, test_name: str, message: str = ""):
        """Assert that values are not equal."""
        passed = not_expected != actual
        details = {
            "not_expected": not_expected,
            "actual": actual,
        }
        full_message = message or "Values are not equal"
        if not passed:
            full_message = f"{message} - Expected different value, got {actual}"
        return self.add_result(test_name, passed, full_message, details)

    def assert_true(self, condition, test_name: str, message: str = ""):
        """Assert that condition is True."""
        full_message = message or "Condition is True"
        if not condition:
            full_message = f"{message} - Condition evaluated to False"
        return self.add_result(test_name, bool(condition), full_message)

    def assert_false(self, condition, test_name: str, message: str = ""):
        """Assert that condition is False."""
        passed = not condition
        full_message = message or "Condition is False"
        if condition:
            full_message = f"{message} - Condition evaluated to True"
        return self.add_result(test_name, passed, full_message)

    def assert_not_none(self, value, test_name: str, message: str = ""):
        """Assert that value is not None."""
        passed = value is not None
        full_message = message or "Value is not None"
        if not passed:
            full_message = f"{message} - Value is None"
        return self.add_result(test_name, passed, full_message)

    def assert_is_none(self, value, test_name: str, message: str = ""):
        """Assert that value is None."""
        passed = value is None
        full_message = message or "Value is None"
        if not passed:
            full_message = f"{message} - Value is not None: {value}"
        return self.add_result(test_name, passed, full_message)

    def assert_in(self, item, container, test_name: str, message: str = ""):
        """Assert that item is in container."""
        passed = item in container
        full_message = message or f"{item} is in container"
        if not passed:
            full_message = f"{message} - {item} not found in container"
        return self.add_result(test_name, passed, full_message)

    def assert_not_in(self, item, container, test_name: str, message: str = ""):
        """Assert that item is not in container."""
        passed = item not in container
        full_message = message or f"{item} is not in container"
        if not passed:
            full_message = f"{message} - {item} found in container"
        return self.add_result(test_name, passed, full_message)

    def assert_isinstance(self, obj, class_or_tuple, test_name: str, message: str = ""):
        """Assert that obj is instance of class_or_tuple."""
        passed = isinstance(obj, class_or_tuple)
        full_message = message or f"Object is instance of {class_or_tuple}"
        if not passed:
            full_message = f"{message} - Object type is {type(obj)}, expected {class_or_tuple}"
        return self.add_result(test_name, passed, full_message)

    def assert_raises(self, exception_class, callable_obj, test_name: str, message: str = ""):
        """Assert that callable raises exception_class."""
        try:
            callable_obj()
            full_message = (
                f"{message} - Expected {exception_class.__name__} but no exception raised"
            )
            return self.add_result(test_name, False, full_message)
        except exception_class:
            full_message = message or f"Raised {exception_class.__name__} as expected"
            return self.add_result(test_name, True, full_message)
        except Exception as exc:
            full_message = (
                f"{message} - Expected {exception_class.__name__}, got {type(exc).__name__}"
            )
            return self.add_result(test_name, False, full_message)

    def report(self):
        """Generate and print test report."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed

        print(f"\n{'='*70}")
        print(f"Test Suite: {self.name}")
        print(f"{'='*70}")

        for result in self.results:
            print(f"  {result}")

        print(f"\n{'-'*70}")
        print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
        print(f"{'='*70}\n")

        return passed, failed
