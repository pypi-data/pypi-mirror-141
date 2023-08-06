import aiohttp
import asyncio
import json
from .exceptions import *

class _BaseClient:
    def __init__(self, *, session: aiohttp.ClientSession):
        self.loop = asyncio.get_event_loop()
        self._session = session
        self._endpoint = "https://holyshit.wtf/"
        self._session_owner = False
        
    @classmethod
    async def create(cls):
        """Create a client without an existing aiohttp session"""
        _session = aiohttp.ClientSession()
        inst = cls(session=_session)
        inst._session_owner = True
        return inst
        
    async def _get_response(self, path: str) -> str:
        """Get a response from the API"""
        async with self._session.get(f"{self._endpoint}/{path}") as r:
            content = await r.text()
            try:
                return json.loads(content, strict=False).get("response", None) # allow control character
            except json.decoder.JSONDecodeError as e:
                raise ContentUnavailable(f"The endpoint you're trying to access isn't returning a valid JSON response - got '{content}'") from e
        
    async def _get_gif(self, path: str):
        """Get a GIF response"""
        return await self._get_response(f"gifs/{path}")
    
    async def close(self):
        return await self._session.close() if self._session and not self._session.closed and self._session_owner else False
    
class Client(_BaseClient):
    async def eightball(self):
        """Get a random Magic 8-Ball response"""
        return await self._get_response("8ball")

    async def insult(self):
        """Get a random 1-word insult"""
        return await self._get_response("insults")

    async def sixdigit(self):
        """Get a random 6-digit number"""
        return await self._get_response("6digit")

    async def pickupline(self):
        """Get a random pickup line"""
        return await self._get_response("pickuplines")

    async def bite(self):
        """Get a random URL to a bite GIF"""
        return await self._get_gif("bite")

    async def cuddle(self):
        """Get a random URL to a cuddle GIF"""
        return await self._get_gif("cuddle")

    async def headpat(self):
        """Get a random URL to a headpat GIF"""
        return await self._get_gif("headpat")

    async def highfive(self):
        """Get a random URL to a high five GIF"""
        return await self._get_gif("highfive")

    async def hug(self):
        """Get a random URL to a hug GIF"""
        return await self._get_gif("hug")

    async def kick(self):
        """Get a random URL to a kick GIF"""
        return await self._get_gif("kick")

    async def kill(self):
        """Get a random URL to a kill GIF"""
        return await self._get_gif("kill")

    async def kiss(self):
        """Get a random URL to a kiss GIF"""
        return await self._get_gif("kiss")

    async def lick(self):
        """Get a random URL to a lick GIF"""
        return await self._get_gif("lick")

    async def poke(self):
        """Get a random URL to a poke GIF"""
        return await self._get_gif("poke")

    async def pout(self):
        """Get a random URL to a pout GIF"""
        return await self._get_gif("pout")

    async def punch(self):
        """Get a random URL to a punch GIF"""
        return await self._get_gif("punch")

    async def slap(self):
        """ Get a random URL to a slap GIF"""
        return await self._get_gif("slap")

    async def stare(self):
        """Get a random URL to a stare GIF"""
        return await self._get_gif("stare")

    async def tickle(self):
        """Get a random URL to a tickle GIF"""
        return await self._get_gif("tickle")

    async def wave(self):
        """Get a random URL to a wave GIF"""
        return await self._get_gif("wave")