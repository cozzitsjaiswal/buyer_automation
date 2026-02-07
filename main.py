import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_numbers = os.getenv('PHONE_NUMBERS').split(',')

async def start_bot():
    clients = []
    for phone in phone_numbers:
        client = TelegramClient(phone, api_id, api_hash)
        await client.start()
        clients.append(client)

        @client.on(events.NewMessage(chats='source_channel'))
        async def handler(event):
            await event.forward_to('destination_channel')

    await asyncio.gather(*[client.run_until_disconnected() for client in clients])

if __name__ == '__main__':
    asyncio.run(start_bot())