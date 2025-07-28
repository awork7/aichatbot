from langchain_community.vectorstores import Chroma  # Updated import
from langchain_community.embeddings import OllamaEmbeddings  # Updated import
import chromadb
from chromadb.config import Settings
import os

class SIBVectorStore:
    def __init__(self, persist_directory="sib_vectordb"):
        self.persist_directory = persist_directory
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # Configure ChromaDB settings
        self.chroma_settings = Settings(
            anonymized_telemetry=False,
            allow_reset=True
        )
        
    def create_vectorstore(self, documents):
        """Create vector store from SIB documents"""
        if not documents:
            raise ValueError("No documents provided for vector store creation")
            
        print("Creating vector store... This may take a few minutes.")
        
        # Ensure directory exists
        os.makedirs(self.persist_directory, exist_ok=True)
        
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name="sib_knowledge_base"
        )
        
        print(f"Vector store created at: {self.persist_directory}")
        return vectorstore
    
    def load_vectorstore(self):
        """Load existing vector store"""
        if os.path.exists(self.persist_directory):
            vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name="sib_knowledge_base"
            )
            return vectorstore
        else:
            raise FileNotFoundError("Vector store not found. Please create it first.")

if __name__ == "__main__":
    from document_processor import SIBDocumentProcessor
    
    # Process documents
    processor = SIBDocumentProcessor()
    documents = processor.load_sib_documents()
    
    if documents:
        # Create vector store
        vs = SIBVectorStore()
        vectorstore = vs.create_vectorstore(documents)
        print("Vector store creation completed successfully!")
    else:
        print("No documents to process. Add documents to sib_data folder first.")
