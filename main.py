from telethon import TelegramClient, events
import asyncio, os

API_ID = int(os.environ.get('API_ID', '37746589'))
API_HASH = os.environ.get('API_HASH', '2e3ee607acf1e04dfe81ad09e5631bd0')
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
    # Sadece bot mesajlarını işle
    if not event.sender or not getattr(event.sender, 'bot', False):
        return
    text = event.raw_text or ''
    t = text.upper()
    if ('BUY' in t or 'SELL' in t) and 'USDT' in t and 'PRICE' in t:
        msg = clean(text)
        print(f'Sinyal: {msg[:80]}')
        await event.delete()
        # Bot API değil, userbot hesabıyla gönder
        await client.send_message(SOURCE_CHAT, msg)

async def main():
    print('Baslıyor...')
    await client.start()
    print('Baglandi!')
    await client.run_until_disconnected()

asyncio.run(main())
