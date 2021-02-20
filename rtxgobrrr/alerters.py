from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel, PeerChat, PeerUser


class TelegramAlerter:
    def __init__(self, config):
        self.config = config
        self.bot = TelegramClient(
            "rtxtelegram", self.config.telegram_api_id, self.config.telegram_api_hash,
        )

    async def start(self):
        await self.bot.start(bot_token=self.config.telegram_bot_token)
        self.enabled = True
        print("> telegram client enabled")

    async def send_alert(self, content):
        for usernames in self.config.telegram_usernames:
            entity = await self.bot.get_entity(usernames)
            await self.bot.send_message(entity=entity, message=content)
