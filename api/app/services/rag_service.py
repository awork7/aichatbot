import os
import time
import glob
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

from langchain_community.llms import Ollama
from app.core.config import Settings
from app.utils.monitoring import track_metrics, LLM_TOKENS
# Remove this line: from app.utils.cache import cache_result

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm: Optional[Ollama] = None
        self.sib_content: Dict[str, str] = {}
        self.is_ready = False
        self.last_content_update = None
        
    async def initialize(self):
        """Initialize RAG service components"""
        try:
            logger.info("Initializing RAG Service...")
            
            # Initialize LLM
            await self._init_llm()
            
            # Load documents
            await self._load_documents()
            
            # Health check
            await self._health_check()
            
            self.is_ready = True
            logger.info("✅ RAG Service initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize RAG Service: {e}")
            raise
    
    async def _init_llm(self):
        """Initialize LLM connection"""
        try:
            self.llm = Ollama(
                model=self.settings.MODEL_NAME,
                base_url=self.settings.OLLAMA_BASE_URL,
                temperature=self.settings.TEMPERATURE,
                timeout=self.settings.MODEL_TIMEOUT
            )
            
            # Test connection
            test_response = await asyncio.to_thread(
                self.llm.invoke, "Hello"
            )
            logger.info(f"LLM connection test: {test_response[:50]}...")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise
    
    async def _load_documents(self):
        """Load SIB documents from data directory"""
        try:
            documents_path = self.settings.DOCUMENTS_PATH
            if not os.path.exists(documents_path):
                logger.warning(f"Documents path not found: {documents_path}")
                return
            
            content = {}
            file_count = 0
            
            # Load text files
            for file_path in glob.glob(os.path.join(documents_path, "*.txt")):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        filename = os.path.basename(file_path)
                        content[filename] = f.read()[:self.settings.CHUNK_SIZE * 3]
                        file_count += 1
                        logger.debug(f"Loaded: {filename}")
                except Exception as e:
                    logger.warning(f"Error loading {file_path}: {e}")
            
            self.sib_content = content
            self.last_content_update = datetime.utcnow()
            
            logger.info(f"Loaded {file_count} documents")
            
        except Exception as e:
            logger.error(f"Failed to load documents: {e}")
            raise
    
    @track_metrics("rag_query")
    # Remove this line: @cache_result(ttl=300)
    async def query(self, message: str, session_id: str = None) -> Dict[str, Any]:
        """Process user query with RAG approach"""
        if not self.is_ready:
            raise RuntimeError("RAG service not ready")
        
        start_time = time.time()
        
        try:
            logger.info(f"Processing query: {message[:100]}...")
            
            # Check if SIB-related
            if not self._is_sib_related(message):
                return {
                    "answer": "I'm Spark, South Indian Bank's AI assistant. I can only help with South Indian Bank related queries.",
                    "sources": [],
                    "response_time": time.time() - start_time,
                    "session_id": session_id
                }
            
            # Find relevant content
            relevant_content = await self._find_relevant_content(message)
            
            if not relevant_content:
                return {
                    "answer": "I couldn't find specific information about that in my South Indian Bank knowledge base. Please try asking about savings accounts, loans, or customer service.",
                    "sources": [],
                    "response_time": time.time() - start_time,
                    "session_id": session_id
                }
            
            # Generate response
            response = await self._generate_response(message, relevant_content)
            
            # Track token usage
            estimated_tokens = len(response.split()) * 1.3  # Rough estimate
            LLM_TOKENS.labels(model=self.settings.MODEL_NAME).inc(estimated_tokens)
            
            return {
                "answer": response,
                "sources": list(relevant_content.keys()),
                "response_time": time.time() - start_time,
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"Query processing failed: {e}")
            return {
                "answer": "I encountered an error processing your question. Please try again or contact support.",
                "sources": [],
                "response_time": time.time() - start_time,
                "session_id": session_id,
                "error": str(e)
            }
    
    async def _find_relevant_content(self, question: str) -> Dict[str, str]:
        """Find relevant content using keyword matching"""
        relevant = {}
        question_words = set(question.lower().split())
        
        # Topic-based keywords
        topic_keywords = {
            "savings": {"savings", "account", "deposit", "balance", "interest"},
            "loans": {"loan", "credit", "mortgage", "home", "personal", "car"},
            "cards": {"card", "credit", "debit", "atm"},
            "service": {"service", "contact", "phone", "email", "branch", "customer"},
            "general": {"bank", "banking", "sib", "south", "indian"}
        }
        
        for filename, content in self.sib_content.items():
            content_lower = content.lower()
            content_words = set(content_lower.split())
            
            # Calculate relevance score
            relevance_score = 0
            
            # Direct word matches
            common_words = question_words.intersection(content_words)
            relevance_score += len(common_words)
            
            # Topic-specific boost
            for topic, keywords in topic_keywords.items():
                question_topics = question_words.intersection(keywords)
                content_topics = content_words.intersection(keywords)
                if question_topics and content_topics:
                    relevance_score += len(question_topics) * 2
            
            if relevance_score > 0:
                relevant[filename] = content[:self.settings.CHUNK_SIZE]
        
        # If no matches, return general content
        if not relevant and self.sib_content:
            first_file = next(iter(self.sib_content))
            relevant[first_file] = self.sib_content[first_file][:self.settings.CHUNK_SIZE]
        
        return dict(list(relevant.items())[:self.settings.MAX_RELEVANT_DOCS])
    
    async def _generate_response(self, question: str, relevant_content: Dict[str, str]) -> str:
        """Generate response using LLM"""
        # Build context
        context = ""
        for filename, content in relevant_content.items():
            context += f"From {filename}:\n{content[:800]}\n\n"
        
        # Create prompt
        prompt = f"""You are Spark, South Indian Bank's AI assistant. Answer based on this information:

Information: {context}

Question: {question}

Instructions:
1. Answer clearly and concisely about South Indian Bank
2. Use only the provided information
3. If information is insufficient, say so
4. Be helpful and professional

Answer:"""
        
        # Generate response
        response = await asyncio.to_thread(self.llm.invoke, prompt)
        return response.strip()
    
    def _is_sib_related(self, question: str) -> bool:
        """Check if question is related to South Indian Bank"""
        sib_keywords = {
            "south indian bank", "sib", "account", "loan", "credit card",
            "deposit", "banking", "atm", "branch", "customer service",
            "interest rate", "savings", "current account", "fd", "rd",
            "spark", "bank", "money", "finance", "payment"
        }
        
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in sib_keywords)
    
    async def _health_check(self):
        """Perform health check on LLM"""
        try:
            test_response = await asyncio.to_thread(
                self.llm.invoke, "Test connection"
            )
            return test_response is not None
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get detailed health status"""
        llm_healthy = await self._health_check()
        
        return {
            "status": "healthy" if (self.is_ready and llm_healthy) else "unhealthy",
            "components": {
                "llm": "healthy" if llm_healthy else "unhealthy",
                "documents": "healthy" if self.sib_content else "unhealthy",
                "last_update": self.last_content_update.isoformat() if self.last_content_update else None
            },
            "metrics": {
                "documents_loaded": len(self.sib_content),
                "model": self.settings.MODEL_NAME
            }
        }
    
    async def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up RAG Service...")
        self.is_ready = False
        #
