"""
CrewAI Tasks for Route-Rakshak Logistics Super-App
Task definitions for AI agents to execute specific logistics operations
"""

from crewai import Task
from agents import get_safety_agent, get_mechanic_agent, get_logistics_agent, get_finance_agent


class LogisticsTasks:
    """
    Collection of specialized tasks for logistics operations
    """
    
    def safety_check_task(self, image_path: str) -> Task:
        """
        Task for safety agent to analyze driver alertness
        """
        return Task(
            description=f"""
            Analyze the driver selfie image at path: {image_path}
            
            Your responsibilities:
            1. Use the drowsiness detection tool to analyze the image
            2. Assess the driver's alertness level and fatigue signs
            3. Provide safety recommendations based on the analysis
            4. If drowsiness is detected, suggest immediate actions
            5. Document the safety assessment for compliance records
            
            Expected Output: A comprehensive safety report with alertness status, 
            risk assessment, and actionable recommendations for driver safety.
            """,
            agent=get_safety_agent(),
            expected_output="Safety assessment report with driver alertness status and recommendations"
        )
    
    def engine_diagnosis_task(self, audio_path: str) -> Task:
        """
        Task for mechanic agent to diagnose engine issues
        """
        return Task(
            description=f"""
            Analyze the engine audio recording at path: {audio_path}
            
            Your responsibilities:
            1. Use the engine diagnosis tool to analyze the audio
            2. Identify any mechanical issues or abnormalities
            3. Assess the severity of any detected problems
            4. Recommend maintenance actions and timeline
            5. Estimate potential costs and downtime if issues are ignored
            
            Expected Output: A detailed diagnostic report with issue identification,
            severity assessment, maintenance recommendations, and cost implications.
            """,
            agent=get_mechanic_agent(),
            expected_output="Engine diagnostic report with issue analysis and maintenance recommendations"
        )
    
    def market_search_task(self, current_location: str) -> Task:
        """
        Task for logistics agent to find profitable return loads
        """
        return Task(
            description=f"""
            Search for profitable return load opportunities from location: {current_location}
            
            Your responsibilities:
            1. Use the market search tool to find available loads
            2. Analyze the profitability and feasibility of each opportunity
            3. Consider factors like distance, delivery time, and client reliability
            4. Recommend the most profitable and strategic load option
            5. Calculate potential revenue and profit margins
            
            Expected Output: A market analysis report with recommended load opportunities,
            revenue projections, and strategic recommendations for maximizing profits.
            """,
            agent=get_logistics_agent(),
            expected_output="Market analysis report with profitable load recommendations and revenue projections"
        )
    
    def expense_validation_task(self, amount: float, item: str, category: str = "General") -> Task:
        """
        Task for finance agent to validate expenses
        """
        return Task(
            description=f"""
            Validate the expense claim: ₹{amount} for {item} in category {category}
            
            Your responsibilities:
            1. Use the expense validator tool to check the claim
            2. Verify compliance with company expense policies
            3. Assess the risk level and approval requirements
            4. Provide detailed justification for approval or rejection
            5. Suggest cost optimization opportunities if applicable
            
            Expected Output: An expense validation report with approval status,
            compliance assessment, and financial recommendations.
            """,
            agent=get_finance_agent(),
            expected_output="Expense validation report with approval status and compliance assessment"
        )
    
    def comprehensive_fleet_analysis_task(self, vehicle_data: dict) -> Task:
        """
        Multi-agent task for comprehensive fleet analysis
        """
        return Task(
            description=f"""
            Conduct a comprehensive analysis of fleet vehicle: {vehicle_data.get('vehicle_id', 'Unknown')}
            
            This is a collaborative task involving multiple aspects:
            1. Safety assessment of the driver
            2. Mechanical condition evaluation
            3. Route optimization and load opportunities
            4. Financial performance and expense validation
            
            Vehicle Data: {vehicle_data}
            
            Expected Output: A comprehensive fleet analysis report covering safety,
            mechanical, logistics, and financial aspects with actionable insights.
            """,
            agent=get_logistics_agent(),  # Lead agent for coordination
            expected_output="Comprehensive fleet analysis report with multi-dimensional insights and recommendations"
        )


# Create task instances for easy import
tasks = LogisticsTasks()

# Example task creation functions for quick access
def create_safety_task(image_path: str) -> Task:
    """Quick function to create a safety check task"""
    return tasks.safety_check_task(image_path)

def create_engine_task(audio_path: str) -> Task:
    """Quick function to create an engine diagnosis task"""
    return tasks.engine_diagnosis_task(audio_path)

def create_market_task(location: str) -> Task:
    """Quick function to create a market search task"""
    return tasks.market_search_task(location)

def create_expense_task(amount: float, item: str, category: str = "General") -> Task:
    """Quick function to create an expense validation task"""
    return tasks.expense_validation_task(amount, item, category)