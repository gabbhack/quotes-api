import secrets
from typing import Dict, Optional

from aiohttp import ClientSession

from app import config


class TelegramFiles:
    def __init__(self, token: str) -> None:
        self.token = token
        self.session: Optional[ClientSession] = None
    
    async def create_session(self):
        if self.session is None or self.session.closed:
            self.session = ClientSession()
        return self.session
    
    async def get_path(self, id: str) -> Optional[str]:
        session = await self.create_session()

        async with session.get(f"https://api.telegram.org/bot{self.token}/getFile?file_id={id}") as resp:
            if resp.status != 200:
                return None
            json = await resp.json()
            path = json["result"]["file_path"]
            return path
    
    async def stream(self, path: str):
        session = await self.create_session()
        
        async with session.get(f"https://api.telegram.org/file/bot{self.token}/{path}") as resp:
            async for chunk in resp.content:
                yield chunk


def generate_api_key() -> str:
    return secrets.token_urlsafe(128)

telegram_files = TelegramFiles(config.TELEGRAM_API_KEY)
