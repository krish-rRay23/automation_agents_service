from crewai import Crew, Agent

# Define agents with required parameters
scraper = Agent(
    role="Extract website data",
    goal="Scrape data from provided URLs",
    backstory="A diligent web scraper designed to extract relevant information from any website."
)
summarizer = Agent(
    role="Summarize scraped data",
    goal="Provide concise summaries",
    backstory="An expert at distilling large amounts of information into clear, actionable summaries."
)
emailer = Agent(
    role="Send reports",
    goal="Email the final summary to the user",
    backstory="A reliable assistant responsible for delivering important reports to users via email."
)

# Crew setup
crew = Crew(agents=[scraper, summarizer, emailer])

# Run the workflow with correct input type
result = crew.kickoff(inputs={"input": "Scrape site and send summary"})
print(result)
