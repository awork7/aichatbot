#!/usr/bin/env python3
import subprocess
import sys
import os
import time

def check_ollama():
    """Check if Ollama is running and models are available"""
    try:
        print("🔍 Checking Ollama installation...")
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            print("❌ Ollama not responding")
            return False
            
        if "llama3.1:8b" not in result.stdout:
            print("❌ Required model not found. Please run:")
            print("   ollama pull llama3.1:8b")
            return False
            
        if "nomic-embed-text" not in result.stdout:
            print("❌ Embedding model not found. Please run:")
            print("   ollama pull nomic-embed-text")
            return False
            
        print("✅ Ollama and models ready!")
        return True
        
    except FileNotFoundError:
        print("❌ Ollama not found. Please install Ollama first.")
        print("   Visit: https://ollama.com")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Ollama not responding. Please start Ollama service.")
        return False

def check_documents():
    """Check if documents exist"""
    if not os.path.exists("sib_data"):
        print("❌ sib_data folder not found")
        return False
    
    files = os.listdir("sib_data")
    if not files:
        print("❌ No documents found in sib_data folder")
        return False
    
    print(f"✅ Found {len(files)} document(s) in sib_data")
    return True

def setup_vectordb():
    """Setup vector database if not exists"""
    if not os.path.exists("sib_vectordb") or not os.listdir("sib_vectordb"):
        print("🔄 Setting up vector database...")
        
        try:
            print("   Processing documents...")
            result = subprocess.run([sys.executable, "document_processor.py"], 
                                 capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                print(f"❌ Document processing failed: {result.stderr}")
                return False
            
            print("   Creating vector store...")
            result = subprocess.run([sys.executable, "vector_store.py"], 
                                 capture_output=True, text=True, timeout=600)
            if result.returncode != 0:
                print(f"❌ Vector store creation failed: {result.stderr}")
                return False
                
            print("✅ Vector database setup complete!")
            
        except subprocess.TimeoutExpired:
            print("❌ Setup timed out. This may indicate insufficient system resources.")
            return False
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False
    else:
        print("✅ Vector database already exists")
    
    return True

def run_chatbot():
    """Run the Streamlit chatbot"""
    print("🚀 Starting South Indian Bank Chatbot...")
    print("   Opening in your default browser...")
    print("   Press Ctrl+C to stop")
    
    try:
        subprocess.run(["streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Chatbot stopped")
    except Exception as e:
        print(f"❌ Failed to start chatbot: {e}")

def main():
    print("🏦 South Indian Bank Chatbot Launcher")
    print("=" * 50)
    
    # Check all prerequisites
    checks = [
        ("Ollama", check_ollama()),
        ("Documents", check_documents()),
    ]
    
    failed_checks = [name for name, status in checks if not status]
    
    if failed_checks:
        print(f"\n❌ Failed checks: {', '.join(failed_checks)}")
        print("\nPlease resolve the issues above and run again.")
        return
    
    # Setup vector database
    if not setup_vectordb():
        print("\n❌ Vector database setup failed")
        return
    
    print("\n" + "=" * 50)
    print("🎉 All systems ready!")
    
    # Run the chatbot
    run_chatbot()

if __name__ == "__main__":
    main()
