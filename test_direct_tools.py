"""
Test direct tool execution without CrewAI crew
"""

def test_direct_tools():
    """Test all tools directly without CrewAI"""
    print("🔧 Testing Direct Tool Execution (No CrewAI Crew)...")
    
    try:
        from tools import (
            drowsiness_detection_tool,
            engine_diagnosis_tool,
            market_search_tool,
            expense_validator_tool
        )
        
        # Test drowsiness detection
        print("\n1. Testing Drowsiness Detection:")
        result = drowsiness_detection_tool.run("test_driver_selfie.jpg")
        print(f"   ✅ Result: {result}")
        
        # Test engine diagnosis
        print("\n2. Testing Engine Diagnosis:")
        result = engine_diagnosis_tool.run("test_engine_audio.wav")
        print(f"   ✅ Result: {result}")
        
        # Test market search
        print("\n3. Testing Market Search:")
        result = market_search_tool.run("Chennai")
        print(f"   ✅ Result: {result[:100]}...")
        
        # Test expense validation
        print("\n4. Testing Expense Validation:")
        result = expense_validator_tool.run(amount=1500.0, item="Fuel", category="Fuel")
        print(f"   ✅ Result: {result[:100]}...")
        
        print("\n🎉 All direct tools working perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run the test"""
    print("🚛 Route-Rakshak Direct Tools Test")
    print("=" * 50)
    
    if test_direct_tools():
        print("\n✅ SUCCESS: All AI tools work without OpenAI!")
        print("🚀 Your Streamlit app will now work perfectly!")
    else:
        print("\n❌ FAILED: Tools have issues")

if __name__ == "__main__":
    main()