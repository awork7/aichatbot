import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader  # Updated import
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

class SIBDocumentProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def load_sib_documents(self, data_folder="sib_data"):
        """Load all South Indian Bank documents"""
        documents = []
        
        if not os.path.exists(data_folder):
            print(f"Creating {data_folder} directory...")
            os.makedirs(data_folder)
            print("Please add your SIB documents to this folder and run again.")
            return []
        
        for filename in os.listdir(data_folder):
            file_path = os.path.join(data_folder, filename)
            
            try:
                if filename.endswith('.pdf'):
                    loader = PyPDFLoader(file_path)
                    docs = loader.load()
                    documents.extend(docs)
                    print(f"Loaded PDF: {filename}")
                elif filename.endswith('.txt'):
                    loader = TextLoader(file_path, encoding='utf-8')
                    docs = loader.load()
                    documents.extend(docs)
                    print(f"Loaded text file: {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        
        if not documents:
            print("No documents found! Please add SIB documents to the sib_data folder.")
            return []
        
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Add metadata to identify SIB-specific content
        for chunk in chunks:
            chunk.metadata['source_type'] = 'south_indian_bank'
            chunk.metadata['domain'] = 'banking'
        
        print(f"Successfully processed {len(chunks)} chunks from {len(documents)} documents")
        return chunks

if __name__ == "__main__":
    processor = SIBDocumentProcessor()
    chunks = processor.load_sib_documents()
