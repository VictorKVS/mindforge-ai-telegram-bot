import asyncio
from src.bot.ai.llm_client import llm_client

async def main():
    print("Тест LLMClient...")
    ans = await llm_client.generate("Привет! Кто ты?")
    print("\nОтвет модели:")
    print(ans)

asyncio.run(main())
