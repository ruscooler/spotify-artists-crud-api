import base64
import datetime
from typing import Dict

import httpx

from app.utils import get_logger, prepare_query_param_for_spotify_api, current_datetime

logger = get_logger(__name__)


class SpotifyAPIClient:
    api_token_url: str = "https://accounts.spotify.com/api/token"
    api_search_url: str = "https://api.spotify.com/v1/search"
    access_token: str = None
    access_token_expires: datetime = current_datetime()

    def __init__(self, client_id: str, client_secret: str) -> None:
        if not (client_id and client_secret):
            raise Exception("You must set client_id and client_secret")
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self) -> str:
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_base64 = base64.b64encode(auth_string.encode())
        return auth_base64.decode()

    async def get_resource_headers(self) -> Dict[str, str]:
        access_token = await self.get_access_token()
        return {
            "Authorization": f"Bearer {access_token}"
        }

    async def perform_auth(self) -> None:
        headers = {
            "Authorization": f"Basic {self.get_client_credentials()}",
        }
        data = {
            "grant_type": "client_credentials"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.api_token_url, data=data, headers=headers)
            response.raise_for_status()
            resp_json = response.json()

        now = current_datetime()
        expires = now + datetime.timedelta(seconds=resp_json['expires_in'])
        self.access_token = resp_json['access_token']
        self.access_token_expires = expires

    async def get_access_token(self):
        if not self.access_token or self.access_token_expires < current_datetime():
            await self.perform_auth()
            return await self.get_access_token()
        return self.access_token

    async def _base_search(self, query_params) -> Dict[str, str]:
        lookup_url = f"{self.api_search_url}?{query_params}"
        headers = await self.get_resource_headers()

        async with httpx.AsyncClient() as client:
            response = await client.get(lookup_url, headers=headers)
            response.raise_for_status()
            return response.json()

    async def get_artists(self, search_dict: Dict[str, str], offset: int = 0, limit: int = 20):
        prepared_query = prepare_query_param_for_spotify_api(search_dict,
                                                             search_type='artist',
                                                             offset=offset,
                                                             limit=limit)
        return await self._base_search(prepared_query)
