import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# 1. Initialize the Search Tool (uses SERPER_API_KEY from environment)
search = SerperDevTool()

# 2. Define the Researcher Agent
researcher = Agent(
    role="Senior Tech News Researcher",
    goal="Discover and summarize today's top 3 breakthrough technology news stories.",
    backstory=(
        "You are an expert tech analyst who specializes in monitoring real-time "
        "tech trends, breakthrough announcements, and industry news."
    ),
    tools=[search],
    verbose=True
)

# 3. Define the Writer Agent (No search tools provided)
writer = Agent(
    role="Tech Newsletter Editor",
    goal="Synthesize research output into a precise, engaging 5-line newsletter.",
    backstory=(
        "You are a concise tech newsletter curator known for distilling complex news "
        "into short, punchy 5-line daily summaries without losing essential context."
    ),
    tools=[],  # Kept empty so the writer focuses solely on writing
    verbose=True
)

# 4. Define Task 1: Find Top 3 Tech Stories
find_task = Task(
    description=(
        "Search the web for today's top 3 trending technology news stories. "
        "Extract the core facts, title, and key takeaway for each story."
    ),
    expected_output=(
        "A structured list containing details for the top 3 tech stories found today."
    ),
    agent=researcher
)

# 5. Define Task 2: Write the 5-Line Newsletter
write_task = Task(
    description=(
        "Take the 3 tech stories provided by the researcher and format them into a newsletter. "
        "The output MUST strictly follow this exact 5-line format:\n"
        "Line 1: Tech in 5 lines\n"
        "Line 2: 1. <first story, one line summary>\n"
        "Line 3: 2. <second story, one line summary>\n"
        "Line 4: 3. <third story, one line summary>\n"
        "Line 5: Why it matters: <one line key takeaway summarizing the broader impact>"
    ),
    expected_output=(
        "A newsletter output containing exactly 5 lines formatted strictly as specified."
    ),
    agent=writer,
    context=[find_task]  # Explicitly handing over Task 1 output to Task 2
)

# 6. Assemble the Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[find_task, write_task],
    process=Process.sequential,
    verbose=True
)

# 7. Kick off execution
if __name__ == "__main__":
    result = crew.kickoff()
    print("\n--- FINAL OUTPUT ---\n")
    print(result)