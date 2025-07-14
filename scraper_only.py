def scraper_agent(state):
    print("📦 Received state:", state)

    # Imagine this is where the robot "scrapes" the page
    url = state["url"]
    scraped = f"Fake scraped content from {url}"

    # Update the state and return it
    new_state = {
        "url": url,
        "scraped_data": scraped
    }

    print("✅ Scraper finished, passing state:", new_state)
    return new_state


# Simulate LangGraph by just running this function manually
input_state = {"url": "https://example.com"}

output_state = scraper_agent(input_state)
