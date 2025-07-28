from langchain_community.llms import Ollama  # Updated import
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from vector_store import SIBVectorStore

class SIBRAGChain:
    def __init__(self, model_name="llama3.1:8b"):
        print("Initializing SIB RAG Chain...")
        try:
            self.llm = Ollama(model=model_name, temperature=0.1)
            self.vector_store = SIBVectorStore()
            self.vectorstore = self.vector_store.load_vectorstore()
            print("RAG Chain initialized successfully!")
        except Exception as e:
            print(f"Error initializing RAG Chain: {e}")
            raise
        
        # Custom prompt for South Indian Bank
        self.prompt_template = """
        You are SOnA (South Indian Bank Online Assistant), an AI assistant specialized in South Indian Bank services, products, and policies.

        Instructions:
        1. ONLY answer questions related to South Indian Bank
        2. If the question is not related to South Indian Bank, politely redirect
        3. Use the provided context to give accurate, helpful responses
        4. Maintain a professional, friendly tone
        5. If you don't have specific information, say so clearly

        Context from South Indian Bank documents:
        {context}

        Human Question: {question}

        SOnA Response:
        """
        
        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "question"]
        )
    
    def create_qa_chain(self):
        """Create the QA chain with retrieval"""
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 4}  # Retrieve top 4 relevant chunks
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": self.prompt},
            return_source_documents=True
        )
        
        return qa_chain
    
    def query(self, question):
        """Query the RAG system"""
        try:
            qa_chain = self.create_qa_chain()
            
            # Check if question is SIB-related
            if not self._is_sib_related(question):
                return {
                    "answer": "I'm SOnA, South Indian Bank's assistant. I can only help with South Indian Bank related queries. Please ask about our banking services, products, or policies.",
                    "sources": []
                }
            
            result = qa_chain({"query": question})
            return {
                "answer": result["result"],
                "sources": [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
            }
        except Exception as e:
            return {
                "answer": f"I encountered an error processing your question: {str(e)}",
                "sources": []
            }
    
    def _is_sib_related(self, question):
        """Basic check if question is related to South Indian Bank"""
        sib_keywords = [
            "south indian bank", "sib", "account", "loan", "credit card",
            "deposit", "banking", "atm", "branch", "customer service",
            "interest rate", "savings", "current account", "fd", "rd",
            "sona", "bank", "money", "finance", "payment"
        ]
        
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in sib_keywords)

if __name__ == "__main__":
    try:
        rag = SIBRAGChain()
        
        # Test query
        response = rag.query("What are the different types of savings accounts in South Indian Bank?")
        print("Answer:", response["answer"])
        print("Sources:", response["sources"])
    except Exception as e:
        print(f"Error: {e}")
