#!/usr/bin/env python3
"""
Pocket - Setup Script
Fase 1: Setup the development environment
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"   ✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ {description} failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False


def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        'logs',
        'sessions', 
        'uploads',
        'exports',
        'tests',
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ Created: {directory}/")
    
    print("✅ All directories created")


def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Not in a virtual environment!")
        print("   Consider creating one with: python -m venv venv")
        response = input("   Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("   Setup cancelled")
            return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        return False
    
    # Install Playwright browsers
    if not run_command("playwright install chromium", "Installing Playwright browsers"):
        return False
    
    return True


def create_env_file():
    """Create .env file from example"""
    env_file = Path('.env')
    env_example = Path('env.example')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        print("📝 Creating .env file from example...")
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ .env file created")
        print("⚠️  Please edit .env file with your Instagram credentials")
        return True
    else:
        print("❌ env.example file not found")
        return False


def test_installation():
    """Test if installation was successful"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        sys.path.append(str(Path(__file__).parent.parent))
        from app.scraper import InstagramScraper
        from app.config import get_settings
        
        print("   ✅ All imports successful")
        return True
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 Pocket - Setup Script")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"📂 Working directory: {project_root}")
    
    # Setup steps
    steps = [
        ("Creating directories", create_directories),
        ("Installing dependencies", install_dependencies),
        ("Creating .env file", create_env_file),
        ("Testing installation", test_installation),
    ]
    
    for step_name, step_function in steps:
        print(f"\n{step_name}...")
        if not step_function():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please fix the error and run setup again")
            sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your Instagram credentials")
    print("2. Run: python scripts/test_instagram.py <username>")
    print("3. If successful, you're ready for Fase 2!")
    
    print("\n🔧 Example test command:")
    print("   python scripts/test_instagram.py cristiano")


if __name__ == "__main__":
    main()
