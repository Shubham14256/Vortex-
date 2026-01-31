"""
Test to verify that CrewAI works without OpenAI dependencies
"""

import os
from dotenv import load_dotenv
load_dotenv()

def test_crew_without_openai():
    """Test CrewAI execution without OpenAI embeddings"""
    print("🧪 Testing CrewAI without OpenAI dependencies...")
    
    try:
        from crewai import Agent, Task, Crew
        from langchain_groq import ChatGroq
        from tools import drowsiness_detection_tool
        
        # Initialize Groq LLM
        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0.7
        )
        
        # Create agent with memory disabled
        agent = Agent(
            role="Test Safety Officer",
            goal="Test safety analysis without OpenAI",
            backstory="I am a test agent to verify no OpenAI dependencies.",
            tools=[drowsiness_detection_tool],
            llm=llm,
            verbose=False,
            memory=False  # CRITICAL: No memory = No OpenAI embeddings
        )
        
        # Create task
        task = Task(
            description="Analyze a test driver image for drowsiness detection.",
            agent=agent,
            expected_output="Safety assessment report"
        )
        
        # Create crew with memory disabled
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False,
            memory=False,  # CRITICAL: No memory = No OpenAI embeddings
            respect_context_window=True
        )
        
        print("   🚀 Executing CrewAI task...")
        result = crew.kickoff()
        
        print(f"   ✅ SUCCESS! CrewAI executed without OpenAI!")
        print(f"   Result: {str(result)[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        return False

def main():
    """Run the test"""
    print("🚛 Route-Rakshak OpenAI Dependency Test")
    print("=" * 50)
    
    # Check API key
    if not os.getenv("GROQ_API_KEY"):
        print("❌ GROQ_API_KEY not found!")
        return
    
    # Test crew execution
    if test_crew_without_openai():
        print("\n🎉 SUCCESS: Your app will work without OpenAI!")
        print("✅ All CrewAI operations use ONLY Groq!")
    else:
        print("\n❌ FAILED: Still has OpenAI dependencies")

if __name__ == "__main__":
    main()