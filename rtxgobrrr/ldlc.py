import asyncio
import aiohttp


class LdlcClient:
    def __init__(self, loop, config, alerter):
        self.loop = loop
        self.config = config
        self.alerter = alerter
        self.last_error = 0
        self.content = None

    async def start(self):
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    self.loop.create_task(self.check_page(session))
                    await asyncio.sleep(self.config.ldlc_delay)
                except Exception:  # we must not stop
                    if time.time() - self.last_error > 60:  # to avoid spamming errors
                        self.alerter.send_alert(f"An error occured: {exception}")
                        self.last_error = time.time()

    async def check_page(self, session):
        output = await self.query_page(session)
        if output:
            if self.content != output:
                if self.content:
                    await self.alerter.send_alert(f"a change has been detected on ldlc page: {self.config.ldlc_url}")
                    self.content = output

    async def query_page(self, session):
        headers = {
            "Referer": self.config.ldlc_referer,
            "User-Agent": self.config.user_agent,
        }
        async with session.get(self.config.ldlc_url, headers=headers) as resp:
            return await resp.text()
