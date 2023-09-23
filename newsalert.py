from uagents import Agent, Context
import requests

news_agent = Agent(name="news_agent", seed="news_agent_seed", port=8890)

def get_top_headlines():
    api_key = "6e447f7d1546441bb6f8f013aa876ef6"
    url = f"https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "country": "in",  # You can change the country code as needed
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    articles = data.get("articles", [])

    headlines = [article["title"] for article in articles]
    return headlines

@news_agent.on_interval(period=3600.0)  # Check every hour (adjust as needed)
async def display_top_headlines(ctx: Context):
    headlines = get_top_headlines()

    for i, headline in enumerate(headlines, start=1):
        ctx.logger.info(f"Headline {i}: {headline}")

if __name__ == "__main__":
    news_agent.run()
