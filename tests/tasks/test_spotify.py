import random

import faker
import pytest
from fastapi import status
from httpx import AsyncClient
from pytest_httpx import HTTPXMock

from app.external.spotify import SpotifyAPIClient
from app.tasks.update_artsits import fetch_artists_from_spotify_periodical
from app.utils import prepare_query_param_for_spotify_api
from tests.utils import generate_spotify_token_api_response, generate_spotify_search_api_response

pytestmark = pytest.mark.anyio
fake = faker.Faker()

spotify_token_url = SpotifyAPIClient.api_token_url
spotify_search_url = SpotifyAPIClient.api_search_url


@pytest.fixture
def non_mocked_hosts() -> list:
    return ["testserver"]


async def test_spotify_api_client_authentication(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=spotify_token_url,
        status_code=status.HTTP_200_OK,
        json=generate_spotify_token_api_response()
    )
    spotify_api_client = SpotifyAPIClient(client_id="client_id", client_secret="client_secret")
    await spotify_api_client.perform_auth()
    assert spotify_api_client.access_token is not None


async def test_spotify_api_client_get_artists(httpx_mock: HTTPXMock, client: AsyncClient, non_mocked_hosts):
    count = 20
    pagination_data = {"offset": 0, "limit": count}
    query_for_search = {
        "year": random.randrange(1960, 2023),
        "genre": fake.word()
    }
    url_path = prepare_query_param_for_spotify_api(query=query_for_search, **pagination_data)
    httpx_mock.add_response(
        url=spotify_token_url,
        status_code=status.HTTP_200_OK,
        json=generate_spotify_token_api_response()
    )
    httpx_mock.add_response(
        url=f"{spotify_search_url}?{url_path}",
        status_code=status.HTTP_200_OK,
        json=generate_spotify_search_api_response(limit=count)
    )
    await fetch_artists_from_spotify_periodical(query_for_search, pagination_data)

    response = await client.get("artists/all")
    assert response.status_code == status.HTTP_200_OK
    saved_artists = response.json()
    assert len(saved_artists) == count

    pagination_data = {"offset": count, "limit": count}
    query_for_search = {
        "year": random.randrange(1960, 2023),
        "genre": fake.word()
    }
    url_path = prepare_query_param_for_spotify_api(query=query_for_search, **pagination_data)
    httpx_mock.add_response(
        url=f"{spotify_search_url}?{url_path}",
        status_code=status.HTTP_200_OK,
        json=generate_spotify_search_api_response(limit=count)
    )
    await fetch_artists_from_spotify_periodical(query_for_search, pagination_data)

    response = await client.get("artists/all")
    assert response.status_code == status.HTTP_200_OK
    saved_artists = response.json()
    assert len(saved_artists) == count * 2
