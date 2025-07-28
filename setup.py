#!/usr/bin/env python3
import os
import subprocess
import sys

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor} detected")
    return True

def install_ollama():
    """Instructions for installing Ollama"""
    print("\n📋 OLLAMA INSTALLATION REQUIRED:")
    print("1. Go to https://ollama.com")
    print("2. Download for Windows")
    print("3. Install the application")
    print("4. Open new Command Prompt and run:")
    print("   ollama pull llama3.1:8b")
    print("   ollama pull nomic-embed-text")
    print("5. Verify with: ollama list")
    
    input("\nPress Enter after completing Ollama installation...")

def setup_environment():
    """Set up the project environment"""
    print("\n🚀 Setting up South Indian Bank Chatbot...")
    
    # Create necessary directories
    print("📁 Creating directories...")
    os.makedirs("sib_data", exist_ok=True)
    os.makedirs("sib_vectordb", exist_ok=True)
    
    # Install Python dependencies
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False
    
    return True

def create_sample_data():
    """Create sample SIB data file"""
    sample_content = """
South Indian Bank - Products and Services

SAVINGS ACCOUNTS:
1. SIB Regular Savings Account
   - Minimum balance: Rs. 1,000
   - Interest rate: 3.5% per annum
   - Features: ATM card, online banking, mobile banking

2. SIB Premium Savings Account
   - Minimum balance: Rs. 25,000
   - Interest rate: 4.0% per annum
   - Features: Premium ATM card, priority banking

LOANS:
1. Personal Loans
   - Interest rate: 11.5% onwards
   - Amount: Up to Rs. 25 lakhs
   - Tenure: Up to 5 years

2. Home Loans
   - Interest rate: 8.5% onwards
   - Amount: Up to Rs. 5 crores
   - Tenure: Up to 30 years

CUSTOMER SERVICE:
- Phone: 1800-102-9090
- Email: customercare@southindianbank.co.in
- WhatsApp Banking: 9895 900 555

BRANCH LOCATIONS:
- Head Office: Thrissur, Kerala
- Branches: 900+ across India
- ATMs: 1,500+ locations
"""
    
    with open("sib_data/sib_sample_data.txt", "w", encoding="utf-8") as f:
        f.write(sample_content)
    
    print("✅ Sample SIB data created!")

if __name__ == "__main__":
    print("🏦 South Indian Bank Chatbot Setup")
    print("=" * 50)
    
    if not check_python():
        exit(1)
    
    install_ollama()
    
    if setup_environment():
        create_sample_data()
        
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Add more SIB documents to 'sib_data' folder")
        print("2. Run: python document_processor.py")
        print("3. Run: python vector_store.py")
        print("4. Run: streamlit run app.py")
        print("\nOr simply run: python run.py")
