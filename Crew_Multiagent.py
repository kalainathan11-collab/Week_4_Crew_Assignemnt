from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
llm=LLM(
    model="gpt-4o-mini",
temperature=0.7   
        )

from crewai import Agent, Task, Crew,llm

# Agent 1
requirement_analyst = Agent(
    role="Requirement Analyst",
    goal="Understand the requirement and identify testable scenarios",
    backstory="You are an experienced QA analyst."
)

# Agent 2
test_case_writer = Agent(
    role="Test Case Designer",
    goal="Create detailed positive and negative test cases",
    backstory="You are an experienced manual QA tester."
)

# Agent 3
reviewer = Agent(
    role="QA Reviewer",
    goal="Review test cases and identify missing scenarios",
    backstory="You are a senior QA lead."
)

# Task for Agent 1
analyze_requirement = Task(
    description="""
    Analyze this requirement:
    'User should be able to transfer inventory from one location to another.'
    
    Identify functional scenarios, validations, and edge cases.
    """,
    expected_output="A list of test scenarios",
    agent=requirement_analyst
)

# Task for Agent 2
create_test_cases = Task(
    description="""
    Using the scenarios identified by the Requirement Analyst,
    create detailed positive and negative test cases.
    """,
    expected_output="Detailed QA test cases",
    agent=test_case_writer
)

# Task for Agent 3
review_test_cases = Task(
    description="""
    Review the generated test cases.
    Identify missing scenarios, boundary cases, and authorization cases.
    """,
    expected_output="Reviewed and improved test cases",
    agent=reviewer
)

# Create the team
qa_crew = Crew(
    agents=[
        requirement_analyst,
        test_case_writer,
        reviewer
    ],
    tasks=[
        analyze_requirement,
        create_test_cases,
        review_test_cases
    ]
)

# Start the crew
result = qa_crew.kickoff()

print(result)