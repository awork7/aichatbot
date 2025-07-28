from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from vector_store import SIBVectorStore
import time

class SIBRAGChain:
    def __init__(self, model_name="llama3.2:1b"):  # Even smaller model

        print("Initializing SIB RAG Chain...")
        try:
            # Use same settings that work in test
            self.llm = Ollama(
                model=model_name,
                temperature=0.1,
                timeout=60,
                base_url="http://localhost:11434"
            )
            
            # Test LLM immediately
            print("Testing LLM connection...")
            test_response = self.llm.invoke("Hi")
            print(f"✅ LLM working: {test_response[:30]}...")
            
            # Load vector store
            print("Loading vector store...")
            self.vector_store = SIBVectorStore()
            self.vectorstore = self.vector_store.load_vectorstore()
            print("✅ Vector store loaded")
            
            # Custom prompt for South Indian Bank
            self.prompt_template = """
You are SOnA (South Indian Bank Online Assistant). Answer briefly and clearly.

Context: {context}
Question: {question}

Answer:"""
            
            self.prompt = PromptTemplate(
                template=self.prompt_template,
                input_variables=["context", "question"]
            )
            
            print("✅ RAG Chain initialized successfully!")
        except Exception as e:
            print(f"❌ Error initializing RAG Chain: {e}")
            raise
    
    def create_qa_chain(self):
        """Create the QA chain with retrieval"""
        try:
            retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": 3}  # Reduced from 4 to 3 for faster processing
            )
            
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": self.prompt},
                return_source_documents=True
            )
            
            return qa_chain
        except Exception as e:
            print(f"❌ Error creating QA chain: {e}")
            raise
    
    def query(self, question):
        """Query the RAG system with detailed logging"""
        try:
            print(f"🔍 Processing query: {question[:50]}...")
            
            # Check if question is SIB-related
            if not self._is_sib_related(question):
                return {
                    "answer": "I'm SOnA, South Indian Bank's assistant. I can only help with South Indian Bank related queries.",
                    "sources": []
                }
            
            print("✅ Query is SIB-related, proceeding...")
            
            # Create QA chain
            print("🔧 Creating QA chain...")
            qa_chain = self.create_qa_chain()
            
            # Execute query with timing
            print("🚀 Executing query...")
            start_time = time.time()
            
            # Use invoke instead of deprecated __call__
            result = qa_chain.invoke({"query": question})
            
            end_time = time.time()
            print(f"✅ Query completed in {end_time - start_time:.2f} seconds")
            
            return {
                "answer": result["result"],
                "sources": [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
            }
            
        except Exception as e:
            error_msg = f"Error processing question: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "answer": error_msg,
                "sources": []
            }
    
    def _is_sib_related(self, question):
        """Check if question is related to South Indian Bank"""
        sib_keywords = [
            "south indian bank", "sib", "account", "loan", "credit card",
            "deposit", "banking", "atm", "branch", "customer service",
            "interest rate", "savings", "current account", "fd", "rd",
            "sona", "bank", "money", "finance", "payment"
        ]
        
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in sib_keywords)

# Test the RAG chain directly
if __name__ == "__main__":
    try:
        print("🧪 Testing RAG Chain...")
        rag = SIBRAGChain()
        
        # Test query
        response = rag.query("What are South Indian Bank savings accounts?")
        print(f"✅ Test Response: {response['answer'][:100]}...")
        print(f"📚 Sources: {response['sources']}")
        
    except Exception as e:
        print(f"❌ RAG Chain test failed: {e}")
