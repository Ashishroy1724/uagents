import requests
from uagents import Agent, Context

# Function to get the current temperature from OpenWeatherMap API
def get_temperature(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "units": "metric",
        "appid": api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        temperature = data["main"]["temp"]
        return temperature
    else:
        raise Exception(f"Error fetching temperature data: {data['message']}")

# Create an agent
temperature_agent = Agent(name="temperature_agent", seed="temperature_agent_seed", port=8888)

# Set your OpenWeatherMap API key
api_key = "e0e25fac6561c99eca026b539e111ccf"
city = "Washington"  # Change this to the city of your choice

@temperature_agent.on_interval(period=30.0)
async def check_temperature(ctx: Context):
    try:
        temperature = get_temperature(api_key, city)

        if temperature > 30:
            ctx.logger.info(f'Temperature is too high: {temperature}°C. Take action!')
        elif temperature < 10:
            ctx.logger.info(f'Temperature is too low: {temperature}°C. Take action!')
        else:
            ctx.logger.info(f'Temperature is normal: {temperature}°C.')

    except Exception as e:
        ctx.logger.error(f"Error: {e}")

if __name__ == "__main__":
    temperature_agent.run()
