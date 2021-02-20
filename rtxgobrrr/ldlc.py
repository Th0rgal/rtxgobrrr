import asyncio
import aiohttp


class LdlcClient:
    def __init__(self, loop, config, alerter):
        self.loop = loop
        self.config = config
        self.alerter = alerter
        self.content = None

    async def start(self):
        while True:
            try:
                self.loop.create_task(self.check_page())
                await asyncio.sleep(self.config.ldlc_delay)
            except Exception:  # we must not stop
                pass

    async def check_page(self):
        output = await self.query_page()
        if output:
            if self.content != output:
                if self.content:
                    await self.alerter.send_alert("a change has been detected")
                else:
                    self.content = output

    async def query_page(self):
        async with aiohttp.ClientSession() as session:
            headers = {
                "Referer": self.config.ldlc_referer,
                "User-Agent": self.config.user_agent,
            }
            async with session.get(self.config.ldlc_url, headers=headers) as resp:
                return await resp.text()
