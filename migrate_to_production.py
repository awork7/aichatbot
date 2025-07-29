#!/usr/bin/env python3
"""
Script to migrate your current SIB chatbot to production structure
"""
import os
import shutil
import json
from pathlib import Path

def migrate_current_code():
    """Migrate current code to production structure"""
    print("🔄 Migrating current code to production structure...")
    
    # Create new structure files with your existing code
    
    # Migrate app.py content to FastAPI structure
    # (This is done by the files provided above)
    
    # Migrate rag_chain.py to services
    if os.path.exists("rag_chain.py"):
        print("✅ rag_chain.py will be integrated into RAGService")
    
    # Migrate document_processor.py to data-pipeline
    if os.path.exists("document_processor.py"):
        shutil.copy("document_processor.py", "data-pipeline/processors/document_processor.py")
        print("✅ Moved document_processor.py to data-pipeline")
    
    # Create package.json for potential React frontend
    frontend_package = {
        "name": "sib-chatbot-frontend",
        "version": "1.0.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "axios": "^1.6.0",
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0",
            "typescript": "^5.0.0"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject"
        }
    }
    
    with open("frontend/package.json", "w") as f:
        json.dump(frontend_package, f, indent=2)
    
    print("✅ Migration completed!")

if __name__ == "__main__":
    migrate_current_code()
