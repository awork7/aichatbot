#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
from pathlib import Path

def create_directory_structure():
    """Create the production directory structure"""
    print("🏗️ Creating production directory structure...")
    
    directories = [
        "api/app/routers", "api/app/models", "api/app/services",
        "api/app/core", "api/app/utils", "api/tests/unit", "api/tests/integration",
        "frontend/src/components", "frontend/src/services", "frontend/public",
        "data-pipeline/processors", "infrastructure/docker", "infrastructure/kubernetes",
        "monitoring/prometheus", "monitoring/grafana", "data/documents",
        "data/embeddings", "data/backups", "scripts", "docs", "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directory structure created")

def migrate_existing_files():
    """Migrate existing files to new structure"""
    print("📦 Migrating existing files...")
    
    migrations = [
        ("sib_data", "data/documents"),
        ("sib_vectordb", "data/embeddings"),
    ]
    
    for source, target in migrations:
        if os.path.exists(source):
            if os.path.exists(target):
                shutil.rmtree(target)
            shutil.move(source, target)
            print(f"✅ Moved {source} to {target}")

def create_config_files():
    """Create configuration files"""
    print("⚙️ Creating configuration files...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        shutil.copy(".env.example", ".env")
        print("✅ Created .env file")
    
    # Create __init__.py files
    init_files = [
        "api/app/__init__.py",
        "api/app/routers/__init__.py",
        "api/app/models/__init__.py",
        "api/app/services/__init__.py",
        "api/app/core/__init__.py",
        "api/app/utils/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
    
    print("✅ Configuration files created")

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "api/requirements.txt"
        ], check=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")

def main():
    print("🏦 SIB Chatbot Production Setup")
    print("=" * 50)
    
    create_directory_structure()
    migrate_existing_files()
    create_config_files()
    install_dependencies()
    
    print("\n🎉 Production setup completed!")
    print("\nNext steps:")
    print("1. Update .env file with your configuration")
    print("2. Add your documents to data/documents/")
    print("3. Run: docker-compose up -d")
    print("4. Access API at: http://localhost:8000")
    print("5. View docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
