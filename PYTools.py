
import os
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool, BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()   

# =====================================================================
# METHOD 1: Define a Function as a Tool using the @tool Decorator
# =====================================================================
@tool("Pharmacy Stock Checker")
def check_pharmacy_stock(ndc_code: str) -> str:
    """Useful to check stock availability and drug details using an 11-digit NDC code."""
    # Mock database lookup
    stock_db = {
        "00002-3228-30": {"name": "Prozac 20mg", "stock": 500, "status": "In Stock"},
        "54868-0001-0": {"name": "Amoxicillin 500mg", "stock": 0, "status": "Out of Stock"}
    }
    
    drug = stock_db.get(ndc_code)
    if drug:
        return f"Drug: {drug['name']} | Stock Count: {drug['stock']} | Status: {drug['status']}"
    return f"NDC code '{ndc_code}' not found in inventory system."


# =====================================================================
# METHOD 2: Define a Class-Based Tool using BaseTool & Pydantic
# =====================================================================
class BenefitValidationInput(BaseModel):
    plan_id: str = Field(..., description="The PBM Plan ID (e.g., 'PLAN_A01')")
    copay_tier: int = Field(..., description="The benefit copay tier integer (e.g., 1, 2, 3)")

class BenefitValidationTool(BaseTool):
    name: str = "Benefit Configuration Validator"
    description: str = "Validates if a specific PBM plan supports a given copay tier level."
    args_schema: type[BaseModel] = BenefitValidationInput

    def _run(self, plan_id: str, copay_tier: int) -> str:
        # Business logic validation
        if plan_id == "PLAN_A01" and copay_tier <= 2:
            return f"Plan '{plan_id}' APPROVED for Tier {copay_tier}. Requires Prior Authorization."
        return f"Plan '{plan_id}' REJECTED for Tier {copay_tier}. Exceeds maximum coverage rules."


# =====================================================================
# AGENTS & TASKS SETUP USING THE DEFINED TOOLS
# =====================================================================

# Define Agent and pass the defined tools
qa_agent = Agent(
    role="PBM & Pharmacy QA Specialist",
    goal="Verify inventory stock and benefit configuration rules for test scenarios.",
    backstory="Senior QA Engineer specializing in healthcare formularies and inventory testing.",
    tools=[check_pharmacy_stock, BenefitValidationTool()], # Attaching custom tools
    verbose=True
)

# Define Task requiring the tools
qa_task = Task(
    description=(
        "1. Check the inventory status for NDC '00002-3228-30'.\n"
        "2. Validate if Plan 'PLAN_A01' supports Copay Tier 2.\n"
        "3. Provide a consolidated QA test result summary."
    ),
    expected_output="A structured report covering stock status and plan validation results.",
    agent=qa_agent
)

# =====================================================================
# EXECUTION PIPELINE
# =====================================================================
if __name__ == "__main__":
    qa_crew = Crew(
        agents=[qa_agent],
        tasks=[qa_task],
        process=Process.sequential,
        verbose=True
    )

    print("\n--- Running CrewAI Pipeline with Custom Function Tools ---\n")
    result = qa_crew.kickoff()
    
    print("\n--- Execution Final Output ---")
    print(result)
