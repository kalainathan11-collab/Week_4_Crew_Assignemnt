import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

# 1. Define inline text directly in the script
inline_text = """
Project Alpha Report - Q3 2026
---------------------------------
Project Manager: Sarah Jenkins
Release Date: October 15, 2026
Budget Allocated: $150,000

Key Milestones:
- Backend infrastructure migrated to serverless architecture on August 10.
- User authentication security audit completed with zero critical vulnerabilities.
- Expected user growth post-launch is estimated at 35% quarter-over-quarter.
"""

# 2. Define the workspace file path and write the content
file_path = "sample_data.txt"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(inline_text)

# 3. Pass the workspace file path to the FileReadTool
file_read_tool = FileReadTool(file_path=file_path)

# 4. Define the Extraction Agent
extractor_agent = Agent(
    role="Information Extraction Specialist",
    goal="Extract precise details from text files.",
    backstory="You are an expert at scanning text documents and extracting key metadata and facts.",
    tools=[file_read_tool],
    verbose=True
)

# 5. Define the Extraction Task
extraction_task = Task(
    description=(
        f"Read the text file using FileReadTool from path: '{file_path}'. "
        "Extract the following information: "
        "1. Project Name and Manager "
        "2. Important Dates and Budget "
        "3. Key Milestones achieved" 
        "4.start date of project"
    ),
    expected_output="A clean summary with key project details and milestone points.",
    agent=extractor_agent
)

# 6. Form and execute the Crew
crew = Crew(
    agents=[extractor_agent],
    tasks=[extraction_task],
    process=Process.sequential,
    memory=True,
    verbose=True
)

result = crew.kickoff()

print("\n================ EXTRACTED INFORMATION ================\n")
print(result)