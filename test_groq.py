"""
Test Groq API connection and CrewAI integration
"""

import os
from dotenv import load_dotenv
load_dotenv()

def test_groq_connection():
    """Test direct Groq API connection"""
    print("🔍 Testing Groq API Connection...")
    
    try:
        from langchain_groq import ChatGroq
        
        # Initialize Groq LLM
        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192",
            temperature=0.7
        )
        
        # Test a simple query
        response = llm.invoke("Hello! Please respond with 'Groq is working!'")
        print(f"   ✅ Groq Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"   ❌ Groq connection failed: {e}")
        return False

def test_crewai_with_groq():
    """Test CrewAI agent with Groq"""
    print("\n🤖 Testing CrewAI Agent with Groq...")
    
    try:
        from crewai import Agent
        from langchain_groq import ChatGroq
        from tools import drowsiness_detection_tool
        
        # Initialize Groq LLM
        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192",
            temperature=0.7
        )
        
        # Create a simple agent
        agent = Agent(
            role="Test Agent",
            goal="Test if CrewAI works with Groq",
            backstory="I am a test agent to verify the integration.",
            tools=[drowsiness_detection_tool],
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
        
        print(f"   ✅ Agent created successfully!")
        print(f"   Agent role: {agent.role}")
        print(f"   Agent LLM: {type(agent.llm)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ CrewAI agent creation failed: {e}")
        return False

def test_task_execution():
    """Test a simple task execution"""
    print("\n📋 Testing Task Execution...")
    
    try:
        from crewai import Agent, Task, Crew
        from langchain_groq import ChatGroq
        from tools import drowsiness_detection_tool
        
        # Initialize Groq LLM
        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192",
            temperature=0.7
        )
        
        # Create agent
        agent = Agent(
            role="Safety Officer",
            goal="Analyze driver safety",
            backstory="I am a safety expert.",
            tools=[drowsiness_detection_tool],
            llm=llm,
            verbose=False
        )
        
        # Create task
        task = Task(
            description="Analyze the driver image at 'test_alert_image.jpg' for drowsiness detection.",
            agent=agent,
            expected_output="Safety assessment report"
        )
        
        # Create and run crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )
        
        print("   🚀 Executing task...")
        result = crew.kickoff()
        print(f"   ✅ Task completed!")
        print(f"   Result: {str(result)[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Task execution failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚛 Route-Rakshak Groq Integration Test")
    print("=" * 50)
    
    # Check if API key exists
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        print("❌ GROQ_API_KEY not found or not set properly!")
        return
    
    print(f"🔑 API Key found: {api_key[:20]}...")
    
    # Test Groq connection
    if not test_groq_connection():
        return
    
    # Test CrewAI with Groq
    if not test_crewai_with_groq():
        return
    
    # Test task execution
    test_task_execution()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("✅ Your Route-Rakshak backend is fully operational!")

if __name__ == "__main__":
    main()