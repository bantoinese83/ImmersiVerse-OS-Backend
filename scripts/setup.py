#!/usr/bin/env python3
"""Setup script for ImmersiVerse OS Backend."""

import os
import sys
import subprocess
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False


def setup_project():
    """Set up the ImmersiVerse OS Backend project."""
    print("🚀 Setting up ImmersiVerse OS Backend...")
    
    # Change to project directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Create virtual environment
    if not Path("venv").exists():
        if not run_command("python -m venv venv", "Creating virtual environment"):
            sys.exit(1)
    
    # Determine activation script
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        activate_script = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Create .env file if it doesn't exist
    if not Path(".env").exists():
        if Path("env.example").exists():
            run_command("cp env.example .env", "Creating .env file from template")
            print("⚠️  Please edit .env file with your configuration")
        else:
            print("⚠️  Please create .env file with your configuration")
    
    # Check if PostgreSQL is available
    if run_command("psql --version", "Checking PostgreSQL"):
        print("✅ PostgreSQL detected")
    else:
        print("⚠️  PostgreSQL not found. Please install PostgreSQL for database functionality")
    
    # Check if Redis is available
    if run_command("redis-cli --version", "Checking Redis"):
        print("✅ Redis detected")
    else:
        print("⚠️  Redis not found. Redis is optional but recommended for caching")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your configuration")
    print("2. Set up your database:")
    print("   - Create PostgreSQL database: createdb immersiverse")
    print("   - Run migrations: alembic upgrade head")
    print("   - Seed data: python scripts/seed_data.py")
    print("3. Start the development server:")
    print("   - uvicorn app.main:app --reload")
    print("4. Access the API documentation at http://localhost:8000/docs")
    print("\nFor Docker setup, run: docker-compose up")


if __name__ == "__main__":
    setup_project()
