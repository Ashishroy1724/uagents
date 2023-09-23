from uagents import Agent, Context
import requests

# Create a currency agent
currency_agent = Agent(name="currency_agent", seed="currency_agent_seed", port=8889)

# API key here
access_key = "4cfb95637d3176a346a4ab7a78b4de60"
url = f"http://apilayer.net/api/live?access_key={access_key}"

def get_exchange_rate(base, target):
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    exchange_rate = data["quotes"][f"{base}{target}"]
    return exchange_rate

@currency_agent.on_interval(period=60.0)
async def check_exchange_rates(ctx: Context):
    amount_usd = float(input("Enter the amount in USD: "))
    target_currency = input("Convert to (EUR, INR, GBP, PLN, CAD, JPY): ").upper()
    
    base = "USD"
    target = target_currency
    
    exchange_rate = get_exchange_rate(base, target)
    
    if exchange_rate is not None:
        converted_amount = amount_usd * exchange_rate
        ctx.logger.info(f'{amount_usd} USD is equivalent to {converted_amount} {target_currency}')
    else:
        ctx.logger.info(f'Invalid currency pair: {base}/{target}')

if __name__ == "__main__":
    currency_agent.run()
