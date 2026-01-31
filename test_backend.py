"""
Test script for Route-Rakshak backend functionality
Tests tools, agents, and tasks without requiring API keys
"""

import time

def test_tools():
    """Test all custom tools"""
    print("🔧 Testing Custom Tools...")
    
    # Import the tool objects
    from tools import drowsiness_detection_tool, engine_diagnosis_tool, market_search_tool, expense_validator_tool
    
    # Test drowsiness detection
    print("\n1. Testing Drowsiness Detection Tool:")
    result = drowsiness_detection_tool.run("driver_selfie_alert.jpg")
    print(f"   Result: {result}")
    
    # Test engine diagnosis
    print("\n2. Testing Engine Diagnosis Tool:")
    result = engine_diagnosis_tool.run("engine_audio_smooth.wav")
    print(f"   Result: {result}")
    
    # Test market search
    print("\n3. Testing Market Search Tool:")
    result = market_search_tool.run("Chennai")
    print(f"   Result: {result[:200]}...")  # Show first 200 chars
    
    # Test expense validator
    print("\n4. Testing Expense Validator Tool:")
    result = expense_validator_tool.run(amount=1500.0, item="Fuel", category="Fuel")
    print(f"   Result: {result[:200]}...")  # Show first 200 chars
    
    print("\n✅ All tools tested successfully!")

def test_imports():
    """Test all imports work correctly"""
    print("📦 Testing Imports...")
    
    try:
        import agents
        print("   ✅ agents.py imported successfully")
        
        import tasks
        print("   ✅ tasks.py imported successfully")
        
        import tools
        print("   ✅ tools.py imported successfully")
        
        print("\n✅ All imports successful!")
        return True
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def test_agent_creation():
    """Test agent creation (requires API key)"""
    print("\n🤖 Testing Agent Creation...")
    
    try:
        from agents import get_safety_agent
        
        # This will only work if GROQ_API_KEY is set
        agent = get_safety_agent()
        print("   ✅ Safety agent created successfully")
        print(f"   Agent role: {agent.role}")
        print(f"   Agent goal: {agent.goal[:50]}...")
        
        return True
    except Exception as e:
        print(f"   ⚠️  Agent creation failed (likely missing API key): {e}")
        return False

def main():
    """Run all tests"""
    print("🚛 Route-Rakshak Backend Testing")
    print("=" * 50)
    
    # Test imports first
    if not test_imports():
        return
    
    # Test tools (no API key required)
    test_tools()
    
    # Test agent creation (requires API key)
    test_agent_creation()
    
    print("\n" + "=" * 50)
    print("🎉 Backend testing completed!")
    print("\nNext steps:")
    print("1. Add your Groq API key to .env file")
    print("2. Run: streamlit run app.py")
    print("3. Test the full application!")

if __name__ == "__main__":
    main()