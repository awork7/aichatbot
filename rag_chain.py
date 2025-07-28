from langchain_community.llms import Ollama
import time
import os
import glob

class SIBRAGChain:
    def __init__(self, model_name="llama3.2:1b"):
        print("Initializing Ultra-Simple SIB Chain...")
        try:
            # Simple LLM setup
            self.llm = Ollama(
                model=model_name,
                temperature=0.1,
                timeout=30,
                base_url="http://localhost:11434"
            )
            
            # Test LLM immediately
            print("Testing LLM connection...")
            test_response = self.llm.invoke("Hi")
            print(f"✅ LLM working: {test_response[:30]}...")
            
            # Load documents directly (no vector search)
            print("Loading SIB documents directly...")
            self.sib_content = self._load_sib_content()
            print("✅ SIB documents loaded")
            
            print("✅ Ultra-Simple SIB Chain initialized successfully!")
        except Exception as e:
            print(f"❌ Error initializing Chain: {e}")
            raise
    
    def _load_sib_content(self):
        """Load SIB content directly from files without vector processing"""
        content = {}
        sib_folder = "sib_data"
        
        if not os.path.exists(sib_folder):
            return {"error": "No sib_data folder found"}
        
        # Read all text and PDF files
        for file_path in glob.glob(os.path.join(sib_folder, "*.txt")):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    filename = os.path.basename(file_path)
                    content[filename] = f.read()[:2000]  # First 2000 chars per file
                    print(f"  ✅ Loaded: {filename}")
            except Exception as e:
                print(f"  ⚠️ Error loading {file_path}: {e}")
        
        return content
    
    def query(self, question):
        """Ultra-simple query without vector search - direct keyword matching"""
        try:
            print(f"🔍 Processing query: {question[:50]}...")
            
            # Check if question is SIB-related
            if not self._is_sib_related(question):
                return {
                    "answer": "I'm SOnA, South Indian Bank's assistant. I can only help with South Indian Bank related queries.",
                    "sources": []
                }
            
            print("✅ Query is SIB-related, proceeding...")
            
            # Find relevant content using simple keyword matching
            print("🔍 Finding relevant content...")
            relevant_content = self._find_relevant_content(question)
            
            if not relevant_content:
                return {
                    "answer": "I couldn't find specific information about that in my South Indian Bank knowledge base. Please try asking about savings accounts, loans, or customer service.",
                    "sources": []
                }
            
            print("📝 Building response...")
            
            # Create simple context from relevant content
            context = ""
            sources = []
            for filename, content in relevant_content.items():
                context += f"{content[:800]}\n\n"  # Limit context size
                sources.append(filename)
            
            # Create simple prompt
            prompt = f"""You are SOnA, South Indian Bank's assistant. Answer based on this information:

Information: {context}

Question: {question}

Answer clearly and concisely about South Indian Bank:"""
            
            # Direct LLM call
            print("🚀 Getting response from LLM...")
            start_time = time.time()
            
            response = self.llm.invoke(prompt)
            
            end_time = time.time()
            print(f"✅ Query completed in {end_time - start_time:.2f} seconds")
            
            return {
                "answer": response,
                "sources": sources
            }
            
        except Exception as e:
            error_msg = f"Error processing question: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "answer": "I encountered an error processing your question. Please try asking about South Indian Bank savings accounts, loans, or customer service.",
                "sources": []
            }
    
    def _find_relevant_content(self, question):
        """Simple keyword-based content matching"""
        relevant = {}
        question_words = question.lower().split()
        
        # Define keyword relevance for different topics
        topic_keywords = {
            "savings": ["savings", "account", "deposit", "balance", "interest"],
            "loans": ["loan", "credit", "mortgage", "home", "personal", "car"],
            "cards": ["card", "credit", "debit", "atm"],
            "service": ["service", "contact", "phone", "email", "branch", "customer"],
            "general": ["bank", "banking", "sib", "south indian"]
        }
        
        for filename, content in self.sib_content.items():
            content_lower = content.lower()
            relevance_score = 0
            
            # Simple scoring based on keyword matches
            for word in question_words:
                if word in content_lower:
                    relevance_score += 1
            
            # Boost score for topic-specific keywords
            for topic, keywords in topic_keywords.items():
                for keyword in keywords:
                    if keyword in question.lower() and keyword in content_lower:
                        relevance_score += 2
            
            # Include content if it has any relevance
            if relevance_score > 0:
                relevant[filename] = content
        
        # If no specific matches, return some general content
        if not relevant and self.sib_content:
            # Return first available content as fallback
            first_file = list(self.sib_content.keys())[0]
            relevant[first_file] = self.sib_content[first_file]
        
        return relevant
    
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

# Test the ultra-simple chain
if __name__ == "__main__":
    try:
        print("🧪 Testing Ultra-Simple SIB Chain...")
        rag = SIBRAGChain()
        
        # Test query
        response = rag.query("What are South Indian Bank savings accounts?")
        print(f"✅ Test Response: {response['answer'][:100]}...")
        print(f"📚 Sources: {response['sources']}")
        
    except Exception as e:
        print(f"❌ Chain test failed: {e}")
