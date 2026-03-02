from telethon import TelegramClient, events
import asyncio, os, httpx

API_ID = int(os.environ.get('API_ID', '37746589'))
API_HASH = os.environ.get('API_HASH', '2e3ee607acf1e04dfe81ad09e5631bd0')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8658568083:AAGmUuSxY356CB03iFq0YnLvbx40OATxMjg')
CHAT_ID = int(os.environ.get('CHAT_ID', '-1003134791575'))
SOURCE_CHAT = int(os.environ.get('SOURCE_CHAT', '-1003134791575'))

client = TelegramClient('session', API_ID, API_HASH)

def clean(text):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        l = line.upper()
        if ('BUY' in l or 'SELL' in l) and 'USDT' in l:
            return '\n'.join(lines[i:])
    return text

@client.on(events.NewMessage(chats=SOURCE_CHAT))
async def handler(event):
    # Sadece bot mesajlarını işle (email2telegram botu)
    if not event.sender or not getattr(event.sender, 'bot', False):
        return
    text = event.raw_text or ''
    t = text.upper()
    if ('BUY' in t or 'SELL' in t) and 'USDT' in t and 'PRICE' in t:
        msg = clean(text)
        print(f'Sinyal: {msg[:80]}')
        async with httpx.AsyncClient() as http:
            await http.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                json={'chat_id': CHAT_ID, 'text': msg})

async def main():
    print('Baslıyor...')
    await client.start()
    print('Baglandi!')
    await client.run_until_disconnected()

asyncio.run(main())
