import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Load environment variables (.env file)
load_dotenv()

# Step 1: Initialize Serper Web Search Tool
search_tool = SerperDevTool()

# Step 2: Define the News Researcher Agent
news_researcher = Agent(
    role="Tamil Nadu News Researcher",
    goal="Search the web for the latest breaking news, politics, and updates regarding Tamil Nadu.",
    backstory=(
        "You are an expert news researcher specializing in South Indian news. "
        "Your mission is to find real-time, accurate updates regarding politics, "
        "governance, and major events in Tamil Nadu."
    ),
    tools=[search_tool],
    verbose=True,
    memory=True
)

# Step 3: Define the News Summarizer Agent
news_writer = Agent(
    role="News Editor & Summarizer",
    goal="Summarize raw news search results into a clean, readable newsletter digest.",
    backstory=(
        "You are a senior journalism editor known for transforming raw news bullet points "
        "into clear, professional, and well-structured summaries."
    ),
    verbose=True
)

# Step 4: Define Tasks for the Crew
research_task = Task(
    description=(
        "Search the web for the latest breaking news, politics, and public policy "
        "updates in Tamil Nadu for today. Retrieve at least 4-5 major current headlines."
    ),
    expected_output=(
        "A detailed list of raw key headlines, sources, and brief descriptions of "
        "the latest events in Tamil Nadu."
    ),
    agent=news_researcher
)

writing_task = Task(
    description=(
        "Take the retrieved news updates from the research task and format them into a "
        "well-structured news digest. Group updates into logical sections like 'Politics', "
        "'Infrastructure & Public Schemes', and 'Other Updates'."
    ),
    expected_output=(
        "A cleanly formatted Markdown report containing a short executive summary "
        "followed by bullet points categorized by topic with source citations."
    ),
    agent=news_writer
)

# Step 5: Assemble and Run the Crew
if __name__ == "__main__":
    crew = Crew(
        agents=[news_researcher, news_writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,  # Researcher runs first, then hands off to Editor
        verbose=True
    )

    print("\n--- Starting Tamil Nadu News Gathering Pipeline ---\n")
    result = crew.kickoff()

    print("\n================ FINAL NEWS REPORT ================\n")
    print(result)