#!/usr/bin/env python3
"""Script to run tests with proper configuration."""

import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run the test suite with proper configuration."""
    print("🧪 Running test suite...")
    
    # Change to project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--cov=app",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--tb=short"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ All tests passed!")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed with exit code {e.returncode}")
        return e.returncode


if __name__ == "__main__":
    import os
    exit_code = run_tests()
    sys.exit(exit_code)
