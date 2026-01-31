"""
Simple test for Groq API with updated model
"""

import os
from dotenv import load_dotenv
load_dotenv()

def test_groq_models():
    """Test different Groq models"""
    print("🔍 Testing Groq API with different models...")
    
    models_to_try = [
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant", 
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ]
    
    for model in models_to_try:
        try:
            from langchain_groq import ChatGroq
            
            print(f"\n   Testing model: {model}")
            llm = ChatGroq(
                api_key=os.getenv("GROQ_API_KEY"),
                model=model,
                temperature=0.7
            )
            
            response = llm.invoke("Hello! Say 'Working' if you can respond.")
            print(f"   ✅ {model}: {response.content}")
            return model  # Return the first working model
            
        except Exception as e:
            print(f"   ❌ {model}: {str(e)[:100]}...")
            continue
    
    return None

def test_agent_with_working_model(model_name):
    """Test CrewAI agent with working model"""
    print(f"\n🤖 Testing CrewAI Agent with {model_name}...")
    
    try:
        from crewai import Agent
        from langchain_groq import ChatGroq
        from tools import drowsiness_detection_tool
        
        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model=model_name,
            temperature=0.7
        )
        
        agent = Agent(
            role="Safety Officer",
            goal="Test agent functionality",
            backstory="I am a test safety officer.",
            tools=[drowsiness_detection_tool],
            llm=llm,
            verbose=False
        )
        
        print(f"   ✅ Agent created successfully with {model_name}!")
        return True
        
    except Exception as e:
        print(f"   ❌ Agent creation failed: {e}")
        return False

def main():
    """Run tests"""
    print("🚛 Route-Rakshak Groq Model Test")
    print("=" * 50)
    
    # Test models
    working_model = test_groq_models()
    
    if working_model:
        print(f"\n🎉 Found working model: {working_model}")
        
        # Test agent with working model
        if test_agent_with_working_model(working_model):
            print(f"\n✅ SUCCESS! Update agents.py to use: {working_model}")
        
    else:
        print("\n❌ No working models found. Check your API key.")

if __name__ == "__main__":
    main()