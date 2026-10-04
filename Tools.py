from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileReadTool
from crewai_tools import DOCXSearchTool
from dotenv import load_dotenv

# ==========================================
# 1. Load environment variables
# ==========================================

load_dotenv()


# ==========================================
# 2. LLM
# ==========================================

llm = LLM(
    model="gpt-4o-mini",
    temperature=0.2
)


# ==========================================
# 3. CREATE FILE READER TOOL
# ==========================================

# Update Section 3 in your script:
file_reader = DOCXSearchTool(
    docx="RequirementFile/OrangeHRM_BRD_Document.docx"
)

# ==========================================
# 4. CREATE AGENT
# ==========================================

requirement_analyst = Agent(
    role="Requirement Analyst",

    goal="""
    Read the BRD and identify all testable requirements
    and test scenarios.
    """,

    backstory="""
    You are an experienced QA analyst.
    You analyze business requirements and identify
    positive, negative, boundary and validation scenarios.
    """,

    tools=[file_reader],

    llm=llm,

    verbose=True
)


# ==========================================
# 5. CREATE TASK
# ==========================================

analyze_requirement = Task(
    description="""
    Read the BRD file using the file reader tool.

    Analyze the requirement and identify:

    1. Functional scenarios
    2. Positive scenarios
    3. Negative scenarios
    4. Boundary scenarios
    5. Validation scenarios
    6. Security scenarios

    Do not invent requirements that are not present
    in the BRD.
    """,

    expected_output="""
    A structured requirement analysis containing
    all identified test scenarios.
    """,

    agent=requirement_analyst
)


# ==========================================
# 6. CREATE CREW
# ==========================================

crew = Crew(
    agents=[requirement_analyst],

    tasks=[analyze_requirement],

    process=Process.sequential,

    verbose=True
)


# ==========================================
# 7. EXECUTE
# ==========================================

result = crew.kickoff()


# ==========================================
# 8. PRINT RESULT
# ==========================================

print("\n")
print("=" * 60)
print("FINAL RESULT")
print("=" * 60)

print(result)