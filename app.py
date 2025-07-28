import streamlit as st
from rag_chain import SIBRAGChain
import time
import os

st.set_page_config(
    page_title="SOnA - South Indian Bank Assistant",
    page_icon="🏦",
    layout="wide"
)

@st.cache_resource
def load_rag_chain():
    """Load RAG chain with caching"""
    try:
        return SIBRAGChain()
    except Exception as e:
        st.error(f"Failed to initialize: {e}")
        return None

def main():
    st.title("🏦 SOnA - South Indian Bank Assistant")
    
    # Check vector database
    if not os.path.exists("sib_vectordb"):
        st.error("⚠️ Vector database not found! Run setup first.")
        return
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm SOnA. Ask me about South Indian Bank services."}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about South Indian Bank..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response
        with st.chat_message("assistant"):
            try:
                with st.spinner("Processing... (may take 30-60 seconds)"):
                    rag_chain = load_rag_chain()
                    
                    if rag_chain:
                        start_time = time.time()
                        response = rag_chain.query(prompt)
                        end_time = time.time()
                        
                        # Display response
                        st.markdown(response["answer"])
                        
                        # Show timing info
                        st.caption(f"⏱️ Responded in {end_time - start_time:.1f} seconds")
                        
                        # Sources
                        if response.get("sources"):
                            with st.expander("📚 Sources"):
                                for source in set(response["sources"]):
                                    if source != "Unknown":
                                        st.write(f"- {source}")
                        
                        # Add to chat history
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": response["answer"]
                        })
                    else:
                        error_msg = "❌ Could not initialize assistant"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": error_msg
                        })
                        
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })

if __name__ == "__main__":
    main()
