"""
CrewAI Agents for Route-Rakshak Logistics Super-App
AI-powered agents for intelligent logistics operations
"""

import os
from crewai import Agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Import tools from tools.py
from tools import (
    drowsiness_detection_tool,
    engine_diagnosis_tool,
    market_search_tool,
    expense_validator_tool
)

# Load environment variables
load_dotenv()

# Initialize LLM - using working Groq model
def get_llm():
    """Get Groq LLM instance with working model"""
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.1-8b-instant",  # Working model (fast and free)
        temperature=0.7
    )


class LogisticsAgents:
    """
    Collection of specialized AI agents for logistics operations
    """
    
    def __init__(self):
        """Initialize the agents factory"""
        self.llm = get_llm()
    
    def safety_agent(self) -> Agent:
        """
        Safety Officer Agent - Monitors driver wellness and safety
        """
        return Agent(
            role="Safety Officer",
            goal="Ensure driver safety by monitoring fatigue levels and alertness through image analysis",
            backstory="""You are an experienced safety officer with 15 years in transportation safety.
            Your expertise lies in identifying signs of driver fatigue and implementing preventive measures.
            You prioritize driver wellbeing and road safety above all operational concerns.
            You have keen observation skills and can detect subtle signs of drowsiness or distraction.""",
            tools=[drowsiness_detection_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            memory=False  # Disable memory to avoid OpenAI embeddings
        )
    
    def mechanic_agent(self) -> Agent:
        """
        Senior Mechanic Agent - Diagnoses vehicle issues through audio analysis
        """
        return Agent(
            role="Senior Mechanic",
            goal="Diagnose vehicle engine problems through audio analysis and recommend maintenance actions",
            backstory="""You are a master mechanic with 20+ years of experience in heavy vehicle maintenance.
            You have an exceptional ear for engine sounds and can identify mechanical issues just by listening.
            Your diagnostic skills have saved countless vehicles from major breakdowns.
            You believe in preventive maintenance and always prioritize vehicle reliability and safety.""",
            tools=[engine_diagnosis_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            memory=False  # Disable memory to avoid OpenAI embeddings
        )
    
    def logistics_agent(self) -> Agent:
        """
        Logistics Manager Agent - Optimizes routes and finds return loads
        """
        return Agent(
            role="Logistics Manager",
            goal="Maximize revenue by finding profitable return loads and optimizing route efficiency",
            backstory="""You are a strategic logistics manager with deep market knowledge and 12 years of experience.
            You excel at identifying profitable cargo opportunities and eliminating empty miles.
            Your network spans across major industrial hubs and you understand market dynamics.
            You focus on maximizing fleet utilization while maintaining service quality and delivery schedules.""",
            tools=[market_search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            memory=False  # Disable memory to avoid OpenAI embeddings
        )
    
    def finance_agent(self) -> Agent:
        """
        Finance Agent - Validates expenses and ensures compliance
        """
        return Agent(
            role="Finance Manager",
            goal="Audit and validate all operational expenses while ensuring policy compliance and cost optimization",
            backstory="""You are a meticulous finance manager with 10 years of experience in transportation accounting.
            You have a sharp eye for expense anomalies and ensure strict adherence to company policies.
            Your expertise in cost analysis helps identify savings opportunities while maintaining operational efficiency.
            You balance cost control with operational needs and maintain transparent financial processes.""",
            tools=[expense_validator_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            memory=False  # Disable memory to avoid OpenAI embeddings
        )


# Create global agents factory
agents_factory = LogisticsAgents()

# Export factory functions for lazy loading
def get_safety_agent():
    """Get safety agent instance"""
    return agents_factory.safety_agent()

def get_mechanic_agent():
    """Get mechanic agent instance"""
    return agents_factory.mechanic_agent()

def get_logistics_agent():
    """Get logistics agent instance"""
    return agents_factory.logistics_agent()

def get_finance_agent():
    """Get finance agent instance"""
    return agents_factory.finance_agent()

def get_all_agents():
    """Get all agents as a list"""
    return [
        get_safety_agent(),
        get_mechanic_agent(), 
        get_logistics_agent(),
        get_finance_agent()
    ]

# For backward compatibility - create agents on demand
def create_agents():
    """Create and return all agents"""
    return {
        'safety': get_safety_agent(),
        'mechanic': get_mechanic_agent(),
        'logistics': get_logistics_agent(),
        'finance': get_finance_agent()
    }