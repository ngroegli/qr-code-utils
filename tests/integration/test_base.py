"""
Base classes for integration tests.
"""
from typing import List
from abc import ABC, abstractmethod


class TestResult:
    """Represents a single test result."""

    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.message = ""

    def set_passed(self, message: str = "Test passed"):
        """Mark the test as passed."""
        self.passed = True
        self.message = message

    def set_failed(self, message: str = "Test failed"):
        """Mark the test as failed."""
        self.passed = False
        self.message = message

    def __str__(self):
        """String representation of the test result."""
        status = "PASS" if self.passed else "FAIL"

        green = "\033[92m"
        red = "\033[91m"
        reset = "\033[0m"

        if self.passed:
            colored_status = f"{green}{status}{reset}"
        else:
            colored_status = f"{red}{status}{reset}"

        return f"{self.name}: {colored_status} - {self.message}"


class BaseIntegrationTest(ABC):
    """Base class for all integration tests."""

    def __init__(self):
        self.name = self.__class__.__name__
        self.results = []

    @abstractmethod
    def run(self) -> List[TestResult]:
        """Run the test and return results."""

    def add_result(self, test_name: str, passed: bool, message: str):
        """Add a test result."""
        result = TestResult(test_name)
        if passed:
            result.set_passed(message)
        else:
            result.set_failed(message)
        self.results.append(result)
        return result

    def report(self):
        """Generate and print test report."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed

        print(f"\n{'='*70}")
        print(f"Integration Test: {self.name}")
        print(f"{'='*70}")

        for result in self.results:
            print(f"  {result}")

        print(f"\n{'-'*70}")
        print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
        print(f"{'='*70}\n")

        return passed, failed
