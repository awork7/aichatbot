# South Indian Bank Chatbot (SOnA)

## Overview
SOnA (South Indian Bank Online Assistant) is an AI-powered chatbot designed exclusively for South Indian Bank queries using RAG (Retrieval-Augmented Generation) approach.

## Features
- 100% offline operation
- RAG-based knowledge retrieval
- South Indian Bank specific responses
- Streamlit web interface
- Free and open-source

## System Requirements
- Windows 10/11
- Python 3.8+
- 16GB RAM (recommended)
- 15GB free disk space

## Quick Start
1. Run setup: `python setup.py`
2. Add SIB documents to `sib_data/` folder
3. Launch: `python run.py`

## File Structure
- `app.py` - Streamlit web interface
- `rag_chain.py` - RAG implementation
- `vector_store.py` - Vector database management
- `document_processor.py` - Document processing
- `sib_data/` - Your SIB documents
- `sib_vectordb/` - Vector database (auto-created)

## Support
For issues, check that:
1. Ollama is running with required models
2. Documents are in sib_data folder
3. Vector database is created
