import random
from uuid import UUID

import pytest
from fastapi import status
from httpx import AsyncClient

from tests.utils import generate_random_artist_payload

pytestmark = pytest.mark.anyio


async def test_get_artists_all(client: AsyncClient):
    response = await client.get("/artists/all")
    assert response.status_code == status.HTTP_200_OK


async def test_add_artist(client: AsyncClient):
    payload = generate_random_artist_payload()
    response = await client.post("/artists/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert payload["spotify_id"] == response.json()["spotify_id"]


async def test_get_artists(client: AsyncClient):
    payload = generate_random_artist_payload()
    response = await client.post("/artists/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    artist_id = response.json()["id"]
    response = await client.get(f"/artists/{artist_id}")
    assert response.status_code == status.HTTP_200_OK
    assert payload["spotify_id"] == response.json()["spotify_id"]
    assert UUID(response.json()["id"])


async def test_delete_artist(client: AsyncClient):
    payload = generate_random_artist_payload()
    response = await client.post("/artists/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    artist_id = response.json()["id"]
    response = await client.delete(f"/artists/{artist_id}")
    assert response.status_code == status.HTTP_200_OK

    response = await client.delete(f"/artists/{artist_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "patch_payload",
    (
        {
            "followers": random.randrange(210, 4000),
        },
    ),
)
async def test_update_artist(client: AsyncClient, patch_payload: dict):
    payload = generate_random_artist_payload()

    response = await client.post("/artists/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    artist_id = response.json()["id"]

    response = await client.patch(f"/artists/{artist_id}", json=patch_payload)
    assert response.status_code == status.HTTP_200_OK

    response = await client.get(f"/artists/{artist_id}")
    assert patch_payload["followers"] == response.json()["followers"]
