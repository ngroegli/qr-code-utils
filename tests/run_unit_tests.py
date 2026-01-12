#!/usr/bin/env python3
"""
Main runner for QR Code Utils unit tests.
"""
import os
import sys
import argparse
import importlib
import inspect
from typing import Dict, Type

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "src"))

# Add tests directory to path for test module imports
tests_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, tests_dir)

# pylint: disable=wrong-import-position
from unit.test_base import BaseUnitTest


def discover_tests() -> Dict[str, Type[BaseUnitTest]]:
    """Dynamically discover all test classes in the unit test directories.

    Returns:
        Dict[str, Type[BaseUnitTest]]: Dictionary of test name to test class
    """
    tests = {}

    # Define the test modules to scan
    test_categories = [
        'common',  # common utilities tests
        'core'     # QR generator tests
    ]

    # Scan each category directory for test modules
    for category in test_categories:
        category_dir = os.path.join(os.path.dirname(__file__), "unit", category)

        if not os.path.isdir(category_dir):
            continue

        # Walk through the category directory
        for root, _, files in os.walk(category_dir):
            rel_path = os.path.relpath(root, os.path.join(os.path.dirname(__file__), "unit"))
            module_prefix = f"unit.{rel_path.replace(os.sep, '.')}"

            for filename in files:
                if filename.startswith("test_") and filename.endswith(".py"):
                    module_name = filename[:-3]  # Remove .py extension
                    full_module_name = f"{module_prefix}.{module_name}"

                    try:
                        # Import the module
                        module = importlib.import_module(full_module_name)

                        # Find all test classes in the module
                        for name, obj in inspect.getmembers(module):
                            if inspect.isclass(obj):
                                if (hasattr(obj, 'run') and
                                    hasattr(obj, 'add_result') and
                                    hasattr(obj, 'report') and
                                    name not in ['BaseUnitTest']):
                                    test_id = f"{rel_path.replace(os.sep, '_')}_{name.lower()}"
                                    tests[test_id] = obj
                    except (ImportError, AttributeError) as exc:
                        print(f"Error importing tests from {full_module_name}: {exc}")

    return tests


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run unit tests for QR Code Utils")
    parser.add_argument(
        "--category",
        choices=["common", "core"],
        help="Run tests from a specific category"
    )
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
    """Main entry point for test runner."""
    args = parse_args()

    # Discover available tests
    all_tests = discover_tests()

    if not all_tests:
        print("No tests found!")
        return 1

    # Handle --list option
    if args.list:
        print("\nAvailable unit tests:")
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
    elif args.category:
        # Run tests from specific category
        tests_to_run = {k: v for k, v in all_tests.items() if k.startswith(args.category)}
    else:
        # Run all tests
        tests_to_run = all_tests

    # Run the tests
    print(f"\n{'='*70}")
    print(f"Running {len(tests_to_run)} test suite(s)")
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
            print(f"ERROR: Test suite {test_id} crashed: {exc}")
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
