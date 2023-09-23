from uagents import Agent, Context
import requests
from datetime import datetime

eventbrite_agent = Agent(name="eventbrite_agent", seed="eventbrite_agent_seed", port=8888)

def get_local_events():
    api_key = 'TXFQ4ATYD2XGH6NPJV'
    url = 'https://www.eventbriteapi.com/v3/events/search/'
    params = {
        'location.latitude': '23°01′17.83″ North',
        'location.longitude': '72°34′46.96″ East',
        'location.within': '10km',
        'start_date.range_start': datetime.utcnow().isoformat() + 'Z',  # Use current UTC time
        'token': api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    events = data.get('events', [])
    return events

@eventbrite_agent.on_interval(period=3600.0)
async def notify_local_events(ctx: Context):
    events = get_local_events()

    if not events:
        ctx.logger.info('No local events found.')
    else:
        ctx.logger.info('Local events:')
        for event in events:
            event_name = event['name']['text']
            event_date = event['start']['local']
            ctx.logger.info(f'{event_name} - {event_date}')

if __name__ == "__main__":
    eventbrite_agent.run()
