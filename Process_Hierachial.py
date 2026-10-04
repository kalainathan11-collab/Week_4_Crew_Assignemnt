from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# 2. CREATE LLM
# ============================================================

llm = LLM(
    model="gpt-4o-mini",
    temperature=0.2
)


# ============================================================
# 3. CREATE AGENTS
# ============================================================

requirement_analyst = Agent(
    role="Requirement Analyst",

    goal="Analyze the requirement and identify all test scenarios.",

    backstory="""
    You are a senior QA analyst.
    You understand business requirements and identify
    positive, negative, boundary, validation and
    authorization scenarios.
    """,

    llm=llm,
    verbose=True
)


test_case_writer = Agent(
    role="Test Case Writer",

    goal="Create detailed and executable QA test cases.",

    backstory="""
    You are an experienced QA test case designer.
    You convert requirements into clear test cases
    with steps, test data and expected results.
    """,

    llm=llm,
    verbose=True
)


test_reviewer = Agent(
    role="Test Case Reviewer",

    goal="Review the test cases and identify missing coverage.",

    backstory="""
    You are a senior QA lead.
    You review test cases for completeness, correctness,
    duplicates and missing scenarios.
    """,

    llm=llm,
    verbose=True
)


# ============================================================
# 4. CREATE TASKS
# ============================================================

requirement_task = Task(
    description="""
    Analyze the following requirement:

    The user should be able to login using a valid
    username and password.

    Identify:

    1. Positive scenarios
    2. Negative scenarios
    3. Boundary scenarios
    4. Validation scenarios
    5. Security scenarios
    6. Authentication scenarios

    Provide a structured requirement analysis.
    """,

    expected_output="""
    A structured list of login test scenarios covering
    positive, negative, boundary, validation and
    security scenarios.
    """
)


test_case_task = Task(
    description="""
    Create detailed manual QA test cases based on
    the requirement analysis.

    Every test case should contain:

    - Test Case ID
    - Test Scenario
    - Preconditions
    - Test Data
    - Test Steps
    - Expected Result
    - Priority
    - Test Type

    Cover positive and negative scenarios.
    """,

    expected_output="""
    A complete list of executable manual QA test cases.
    """
)


review_task = Task(
    description="""
    Review the generated test cases.

    Check:

    1. Requirement coverage
    2. Positive scenarios
    3. Negative scenarios
    4. Boundary scenarios
    5. Validation scenarios
    6. Security scenarios
    7. Duplicate test cases
    8. Incorrect expected results

    Identify missing scenarios and provide the corrected
    final test cases.
    """,

    expected_output="""
    A QA review report and final corrected test cases.
    """
)


# ============================================================
# 5. CREATE HIERARCHICAL CREW
# ============================================================

crew = Crew(
    agents=[
        requirement_analyst,
        test_case_writer,
        test_reviewer
    ],

    tasks=[
        requirement_task,
        test_case_task,
        review_task
    ],

    process=Process.hierarchical,

    # VERY IMPORTANT:
    # Hierarchical process requires a manager LLM
    manager_llm=llm,

    verbose=True
)


# ============================================================
# 6. EXECUTE CREW
# ============================================================

print("\n")
print("=" * 70)
print("STARTING CREWAI HIERARCHICAL PROCESS")
print("=" * 70)

result = crew.kickoff()


# ============================================================
# 7. PRINT FINAL RESULT
# ============================================================

print("\n")
print("=" * 70)
print("FINAL RESULT")
print("=" * 70)

print(result)

print("\n")
print("=" * 70)
print("PROCESS COMPLETED")
print("=" * 70)