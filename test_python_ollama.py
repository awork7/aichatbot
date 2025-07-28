from langchain_community.llms import Ollama
import time

def test_python_ollama():
    print("Testing Python -> Ollama connection...")
    try:
        # Test with same model that works in CLI
        llm = Ollama(
            model="llama3.1:8b",
            temperature=0.1,
            timeout=30,
            base_url="http://localhost:11434"
        )
        
        print("Sending query through Python...")
        start_time = time.time()
        response = llm.invoke("Hello, can you respond with just 'Yes'?")
        end_time = time.time()
        
        print(f"✅ Success! Response: {response}")
        print(f"⏱️ Time taken: {end_time - start_time:.2f} seconds")
        return True
        
    except Exception as e:
        print(f"❌ Python connection failed: {e}")
        return False

if __name__ == "__main__":
    test_python_ollama()
