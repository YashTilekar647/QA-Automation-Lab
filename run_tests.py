"""
run_tests.py – Entry point to run the entire test suite.

Usage:
    python run_tests.py            # run all tests
    python run_tests.py --api      # run only API tests
    python run_tests.py --ui       # run only UI tests
"""

import sys
import pytest


def main():
    """Parse simple CLI flags and invoke pytest."""

    # Default: run everything inside the tests/ folder
    args = ["tests/", "-v", "--tb=short"]

    if "--api" in sys.argv:
        # Run only API tests
        args = ["tests/test_api.py", "-v", "--tb=short"]
    elif "--ui" in sys.argv:
        # Run only UI tests
        args = ["tests/test_ui.py", "-v", "--tb=short"]

    print("=" * 60)
    print("  QA Automation Lab – Running Tests")
    print("=" * 60)
    print(f"  pytest args: {args}")
    print("=" * 60)

    # Exit with the same code pytest returns (0 = all passed)
    exit_code = pytest.main(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
