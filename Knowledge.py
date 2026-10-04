import os
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

load_dotenv()

# -------------------------------------------------
# 0. Ensure the 'knowledge' folder and file exist
# -------------------------------------------------

# Create the 'knowledge' folder if it doesn't exist
os.makedirs("knowledge", exist_ok=True)

# Write the file inside the 'knowledge' folder
file_path = os.path.join("knowledge", "sample_brd.txt")

brd_content = """
Business Requirement Document (BRD) - User Portal
---------------------------------------------------
1. User Authentication:
   - System shall allow users to log in with email and password.
   - Password must be between 8 and 20 characters, containing at least 1 uppercase and 1 number.
   - Account locks after 3 failed consecutive login attempts.

2. Leave Request Module:
   - Employees can apply for leave between 1 and 30 consecutive days.
   - Leave requests must be submitted at least 48 hours prior to start date.
   - System must check leave balance before submission.
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(brd_content)

# -------------------------------------------------
# 1. External Knowledge Source
# -------------------------------------------------

# Point directly to "sample_brd.txt" inside the knowledge folder
brd_knowledge = TextFileKnowledgeSource(
    file_paths=["sample_brd.txt"]
)

# -------------------------------------------------
# 2. Agent
# -------------------------------------------------

requirement_analyst = Agent(
    role="Requirement Analyst",
    goal="Understand the business requirements and identify testable scenarios",
    backstory=(
        "You are an experienced QA analyst who analyzes BRDs "
        "and converts requirements into clear test scenarios."
    ),
    verbose=True
)

# -------------------------------------------------
# 3. Task
# -------------------------------------------------

analyze_brd = Task(
    description="""
    Read the BRD available in the external knowledge source.

    Identify:
    1. Functional requirements
    2. Positive test scenarios
    3. Negative test scenarios
    4. Boundary scenarios
    5. Important acceptance criteria

    Provide the results in a clear table.
    """,
    expected_output="""
    A structured list of requirements and test scenarios.
    """,
    agent=requirement_analyst
)

# -------------------------------------------------
# 4. Crew
# -------------------------------------------------

crew = Crew(
    agents=[requirement_analyst],
    tasks=[analyze_brd],
    process=Process.sequential,

    # Connect external knowledge
    knowledge_sources=[brd_knowledge],

    verbose=True
)

# -------------------------------------------------
# 5. Execute
# -------------------------------------------------

result = crew.kickoff()

print("\n========== RESULT ==========\n")
print(result)