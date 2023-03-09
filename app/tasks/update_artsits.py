import datetime
import json
import random

from faker import Faker

from app import config
from app.database import AsyncSessionFactory
from app.external.spotify import SpotifyAPIClient
from app.models.artist import Artist
from app.models.background_task import BackgroundTask
from app.schemas.artist import ArtistSchema
from app.utils import get_logger

global_settings = config.get_settings()
logger = get_logger(__name__)
fake = Faker()
task_name = "fetch_artists_from_spotify_periodical"


async def fetch_artists_from_spotify_periodical(query_for_search=None, pagination_data=None):
    async with AsyncSessionFactory() as db_session:
        task_db = await BackgroundTask.get_by_name(db_session, task_name)

    if not query_for_search:
        query_for_search = {
            "year": random.randrange(1960, 2023),
            "genre": fake.word()
        }

    if not pagination_data:
        pagination_data = {'offset': 0, 'limit': 20}

    if not task_db:
        task_db = BackgroundTask(task_name=task_name,
                                 data=json.dumps(pagination_data),
                                 last_finished_time=datetime.datetime.utcnow())
    else:
        pagination_data = json.loads(task_db.data)

    spotify_api_client = SpotifyAPIClient(client_id=global_settings.SPOTIFY_CLIENT_ID,
                                          client_secret=global_settings.SPOTIFY_CLIENT_SECRET)
    artists_list = await spotify_api_client.get_artists(query_for_search, **pagination_data)

    async with AsyncSessionFactory() as db_session:
        for item in artists_list['artists']['items']:
            artist_pre_obj = ArtistSchema(
                spotify_id=item['id'],
                name=item['name'],
                type=item['type'],
                followers=item['followers']['total'],
                popularity=item['popularity'],
                genres=item['genres'],
                image_url=item['images'][0]['url'] if item.get('images') else None,
            )

            artist_obj = Artist(**artist_pre_obj.dict())
            await Artist.update_or_create(db_session, artist_obj)

        pagination_data['offset'] += pagination_data['limit']
        task_db.data = json.dumps(pagination_data)
        task_db.is_success = True

        await task_db.save(db_session)
