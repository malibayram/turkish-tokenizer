#!/usr/bin/env python3
"""
Script to create a new release and tag for automated PyPI publishing.
"""

import subprocess
import sys
import re
from pathlib import Path

def get_current_version():
    """Get current version from pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("❌ pyproject.toml not found")
        sys.exit(1)
    
    with open(pyproject_path, 'r') as f:
        content = f.read()
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
        else:
            print("❌ Could not find version in pyproject.toml")
            sys.exit(1)

def create_tag_and_release(version):
    """Create a git tag and push it"""
    tag_name = f"v{version}"
    
    print(f"🎯 Creating release for version {version}")
    
    # Check if tag already exists
    try:
        result = subprocess.run(['git', 'tag', '-l', tag_name], 
                              capture_output=True, text=True, check=True)
        if tag_name in result.stdout:
            print(f"⚠️  Tag {tag_name} already exists")
            response = input("Do you want to delete and recreate it? (y/N): ")
            if response.lower() == 'y':
                subprocess.run(['git', 'tag', '-d', tag_name], check=True)
                subprocess.run(['git', 'push', 'origin', ':refs/tags/' + tag_name], 
                             check=True)
            else:
                print("❌ Aborted")
                sys.exit(1)
    except subprocess.CalledProcessError:
        pass
    
    # Create and push tag
    try:
        subprocess.run(['git', 'tag', tag_name], check=True)
        print(f"✅ Created tag {tag_name}")
        
        subprocess.run(['git', 'push', 'origin', tag_name], check=True)
        print(f"✅ Pushed tag {tag_name} to remote")
        
        print(f"\n🎉 Release {tag_name} created successfully!")
        print(f"📦 GitHub Actions will automatically publish to PyPI")
        print(f"🔗 Check the Actions tab for progress: https://github.com/malibayram/turkish-tokenizer/actions")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating tag: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) > 1:
        version = sys.argv[1]
    else:
        version = get_current_version()
        print(f"📦 Current version: {version}")
    
    create_tag_and_release(version)

if __name__ == "__main__":
    main()
