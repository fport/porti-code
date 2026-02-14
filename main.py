from typing import Any
from client.llm_client import LLMClient
import asyncio
import click


async def run(messages: dict[str, Any]):
    client = LLMClient()
    async for event in client.chat_completion(messages, True):
        print(event)


@click.command()
@click.argument("prompt", required=False)
def main(
    prompt: str,
):
    print(prompt)
    messages = [{"role": "user", "content": prompt}]
    asyncio.run(run(messages))
    print("done")


main()
