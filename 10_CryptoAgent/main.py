
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool
from dotenv import load_dotenv
import os
import requests

# Load API key from .env
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

#  Set up Gemini-compatible client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Gemini model setup
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)

# Agent run configuration
config = RunConfig(
    model=model,
    tracing_disabled=True
)

# Tool to get crypto price from CoinLore API
@function_tool
def get_crypto_price(symbol: str) -> str:
    """
    Gets live crypto price for a given symbol like BTC, ETH.
    """
    try:
        url = "https://api.coinlore.net/api/tickers/"
        response = requests.get(url)
        coins = response.json()["data"]

        for coin in coins:
            if coin["symbol"].upper() == symbol.upper():
                return (
                    f"{coin['name']} ({coin['symbol']}):\n"
                    f"💲 Price: ${coin['price_usd']}\n"
                    f"📈 Change (24h): {coin['percent_change_24h']}%\n"
                    f"🔢 Market Cap: ${coin['market_cap_usd']}\n"
                    f"📊 Volume (24h): ${coin['volume24']}"
                )

        return f"❌ Symbol '{symbol}' not found. Try BTC, ETH, etc."
    
    except Exception as e:
        return f"❌ Error fetching data: {str(e)}"

# define the agent
crypto_agent = Agent(
    name="CryptoDataAgent",
    instructions="You are a helpful agent that provides live cryptocurrency data.",
    tools=[get_crypto_price]
)
            
# Function to run the agent
def run_crypto_agent(user_input):
    response = Runner.run_sync(crypto_agent, input=user_input, config=config)
    return response.final_output
    
            