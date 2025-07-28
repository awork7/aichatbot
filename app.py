import streamlit as st
from rag_chain import SIBRAGChain
import time
import os

# Page configuration
st.set_page_config(
    page_title="SOnA - South Indian Bank Assistant",
    page_icon="🏦",
    layout="wide"
)

# Initialize the RAG chain
@st.cache_resource
def load_rag_chain():
    try:
        return SIBRAGChain()
    except Exception as e:
        st.error(f"Failed to initialize RAG chain: {e}")
        return None

# Custom CSS
st.markdown("""
<style>
    .stChat {
        background-color: #f0f2f6;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #007bff;
        color: white;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #28a745;
        color: white;
        margin-right: 20%;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🏦 SOnA - South Indian Bank Assistant")
    st.subheader("Your AI-powered banking companion")
    
    # Check if vector store exists
    if not os.path.exists("sib_vectordb"):
        st.error("⚠️ Vector database not found!")
        st.write("Please follow these steps:")
        st.write("1. Add your SIB documents to the 'sib_data' folder")
        st.write("2. Run: `python document_processor.py`")
        st.write("3. Run: `python vector_store.py`")
        st.write("4. Refresh this page")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("About SOnA")
        st.write("""
        SOnA (South Indian Bank Online Assistant) is your dedicated AI assistant for all South Indian Bank related queries.
        
        **What I can help you with:**
        - Account services and products
        - Loan information
        - Credit card details
        - Banking policies
        - Branch and ATM locations
        - Interest rates
        - Customer service
        """)
        
        st.header("System Status")
        st.success("🟢 Online - Running locally")
        st.info("🔒 Fully secure - No data leaves your server")
        
        # System info
        st.header("System Info")
        st.write(f"Vector DB: {'✅ Ready' if os.path.exists('sib_vectordb') else '❌ Missing'}")
        st.write(f"Documents: {'✅ Loaded' if os.path.exists('sib_data') else '❌ Missing'}")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm SOnA, your South Indian Bank assistant. How can I help you today?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about South Indian Bank services..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    rag_chain = load_rag_chain()
                    if rag_chain:
                        response = rag_chain.query(prompt)
                        
                        # Display answer
                        st.markdown(response["answer"])
                        
                        # Display sources if available
                        if response["sources"] and any(response["sources"]):
                            with st.expander("📚 Sources"):
                                for source in set(response["sources"]):
                                    if source != "Unknown":
                                        st.write(f"- {source}")
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
                    else:
                        error_msg = "Failed to initialize the assistant. Please check the setup."
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
                except Exception as e:
                    error_msg = f"I'm experiencing some technical difficulties. Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
