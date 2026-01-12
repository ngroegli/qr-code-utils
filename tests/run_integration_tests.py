#!/usr/bin/env python3
"""
Main runner for QR Code Utils integration tests.
"""
import os
import sys
import argparse
import importlib
import inspect
from typing import Dict, Type

# Add the project root and src directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "src"))

# pylint: disable=wrong-import-position
from tests.integration.test_base import BaseIntegrationTest


def discover_tests() -> Dict[str, Type[BaseIntegrationTest]]:
    """Dynamically discover all test classes in the integration test directory.

    Returns:
        Dict[str, Type[BaseIntegrationTest]]: Dictionary of test name to test class
    """
    tests = {}
    integration_dir = os.path.join(os.path.dirname(__file__), "integration")

    if not os.path.isdir(integration_dir):
        return tests

    # Find all Python files in the integration directory
    for filename in os.listdir(integration_dir):
        if filename.startswith("test_") and filename.endswith(".py"):
            module_name = filename[:-3]  # Remove .py extension
            full_module_name = f"tests.integration.{module_name}"

            try:
                # Import the module
                module = importlib.import_module(full_module_name)

                # Find all test classes in the module
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and
                        issubclass(obj, BaseIntegrationTest) and
                        obj != BaseIntegrationTest):
                        test_id = f"{module_name}_{name.lower()}"
                        tests[test_id] = obj
            except (ImportError, AttributeError) as exc:
                print(f"Error importing tests from {full_module_name}: {exc}")

    return tests


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run integration tests for QR Code Utils")
    parser.add_argument(
        "--test",
        type=str,
        help="Run a specific test by name"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available tests without running them"
    )

    return parser.parse_args()


def main():
    """Main entry point for integration test runner."""
    args = parse_args()

    # Discover available tests
    all_tests = discover_tests()

    if not all_tests:
        print("No integration tests found!")
        return 1

    # Handle --list option
    if args.list:
        print("\nAvailable integration tests:")
        print("-" * 70)
        for test_id in sorted(all_tests.keys()):
            print(f"  {test_id}")
        print(f"\nTotal: {len(all_tests)} tests")
        return 0

    # Filter tests based on arguments
    tests_to_run = {}

    if args.test:
        # Run specific test
        matching_tests = {k: v for k, v in all_tests.items() if args.test.lower() in k.lower()}
        if not matching_tests:
            print(f"No test found matching: {args.test}")
            return 1
        tests_to_run = matching_tests
    else:
        # Run all tests
        tests_to_run = all_tests

    # Run the tests
    print(f"\n{'='*70}")
    print(f"Running {len(tests_to_run)} integration test(s)")
    print(f"{'='*70}\n")

    total_passed = 0
    total_failed = 0

    for test_id, test_class in sorted(tests_to_run.items()):
        try:
            test_instance = test_class()
            test_instance.run()
            passed, failed = test_instance.report()
            total_passed += passed
            total_failed += failed
        except Exception as exc:
            print(f"\n{'='*70}")
            print(f"ERROR: Test {test_id} crashed: {exc}")
            print(f"{'='*70}\n")
            total_failed += 1

    # Print summary
    print(f"\n{'='*70}")
    print("OVERALL SUMMARY")
    print(f"{'='*70}")
    print(f"Total Tests Run: {total_passed + total_failed}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"{'='*70}\n")

    # Exit with appropriate code
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
