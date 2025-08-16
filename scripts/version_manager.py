#!/usr/bin/env python3
"""
Version Manager for Turkish Tokenizer

This script provides utilities for managing version numbers across the project.
It can increment major, minor, or patch versions and update all relevant files.
"""

import re
import sys
import os
from pathlib import Path


class VersionManager:
    """Manages version numbers across the project."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.version_files = [
            self.project_root / "pyproject.toml",
            self.project_root / "setup.py",
            self.project_root / "turkish_tokenizer" / "__init__.py"
        ]
    
    def get_current_version(self) -> str:
        """Get the current version from pyproject.toml."""
        pyproject_path = self.project_root / "pyproject.toml"
        
        with open(pyproject_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.search(r'version\s*=\s*"([^"]+)"', content)
        if match:
            return match.group(1)
        else:
            raise ValueError("Could not find version in pyproject.toml")
    
    def parse_version(self, version: str) -> tuple:
        """Parse version string into major, minor, patch components."""
        parts = version.split('.')
        if len(parts) != 3:
            raise ValueError(f"Invalid version format: {version}")
        
        return tuple(int(part) for part in parts)
    
    def format_version(self, major: int, minor: int, patch: int) -> str:
        """Format version components into version string."""
        return f"{major}.{minor}.{patch}"
    
    def increment_version(self, version: str, increment_type: str = 'patch') -> str:
        """Increment version by the specified type."""
        major, minor, patch = self.parse_version(version)
        
        if increment_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif increment_type == 'minor':
            minor += 1
            patch = 0
        elif increment_type == 'patch':
            patch += 1
        else:
            raise ValueError(f"Invalid increment type: {increment_type}")
        
        return self.format_version(major, minor, patch)
    
    def update_file_version(self, file_path: Path, old_version: str, new_version: str):
        """Update version in a specific file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Different patterns for different file types
        if file_path.name == 'pyproject.toml':
            pattern = r'version\s*=\s*"([^"]+)"'
            replacement = f'version = "{new_version}"'
        elif file_path.name == 'setup.py':
            pattern = r'version="([^"]+)"'
            replacement = f'version="{new_version}"'
        elif file_path.name == '__init__.py':
            pattern = r'__version__\s*=\s*"([^"]+)"'
            replacement = f'__version__ = "{new_version}"'
        else:
            raise ValueError(f"Unknown file type: {file_path.name}")
        
        new_content = re.sub(pattern, replacement, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    def update_all_versions(self, new_version: str):
        """Update version in all relevant files."""
        current_version = self.get_current_version()
        
        print(f"🔄 Updating version from {current_version} to {new_version}")
        
        for file_path in self.version_files:
            if file_path.exists():
                self.update_file_version(file_path, current_version, new_version)
                print(f"✅ Updated {file_path.name}")
            else:
                print(f"⚠️  File not found: {file_path}")
    
    def bump_version(self, increment_type: str = 'patch'):
        """Bump version by the specified type."""
        current_version = self.get_current_version()
        new_version = self.increment_version(current_version, increment_type)
        
        self.update_all_versions(new_version)
        print(f"🎉 Version bumped to {new_version}")
        
        return new_version
    
    def set_version(self, version: str):
        """Set version to a specific value."""
        # Validate version format
        try:
            self.parse_version(version)
        except ValueError as e:
            print(f"❌ Invalid version format: {e}")
            return
        
        self.update_all_versions(version)
        print(f"🎯 Version set to {version}")


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/version_manager.py bump [major|minor|patch]")
        print("  python scripts/version_manager.py set <version>")
        print("  python scripts/version_manager.py current")
        sys.exit(1)
    
    manager = VersionManager()
    command = sys.argv[1]
    
    try:
        if command == 'bump':
            increment_type = sys.argv[2] if len(sys.argv) > 2 else 'patch'
            manager.bump_version(increment_type)
        
        elif command == 'set':
            if len(sys.argv) < 3:
                print("❌ Version required for 'set' command")
                sys.exit(1)
            version = sys.argv[2]
            manager.set_version(version)
        
        elif command == 'current':
            version = manager.get_current_version()
            print(f"📦 Current version: {version}")
        
        else:
            print(f"❌ Unknown command: {command}")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
