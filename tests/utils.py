import random
import string

from faker import Faker

fake = Faker()


def generate_random_alpha_numeric_string(size=64):
    chars = string.ascii_lowercase+string.ascii_uppercase+string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def generate_random_artist_payload():
    return {
        "spotify_id": fake.pystr(min_chars=22, max_chars=22),
        "name": f"{fake.first_name()} {fake.last_name()}",
        "followers": random.randrange(1000, 9999999),
        "genres": [fake.word() for _ in range(random.randint(1, 5))],
        "type": "artist",
        "popularity": random.randrange(0, 100),
        "image_url": fake.url(),
    }


def generate_spotify_token_api_response():
    return {
        "access_token": generate_random_alpha_numeric_string(size=116),
        "token_type": "Bearer",
        "expires_in": 3600
    }


def generate_spotify_search_api_response(limit=10):
    items = []
    for _ in range(limit):
        fake_spotify_url = fake.pystr(min_chars=22, max_chars=22)
        items.append({
            "external_urls": {
                "spotify": f"https://open.spotify.com/artist/{fake_spotify_url}"
            },
            "followers": {
                "href": None,
                "total": random.randrange(100, 50_000_000)
            },
            "genres": [fake.word() for _ in range(random.randint(1, 5))],
            "href": f"https://api.spotify.com/v1/artists/{fake_spotify_url}",
            "id": fake_spotify_url,
            "images": [{
                "url": fake.url(),
                "height": 640,
                "width": 640
            }],
            "name": fake.name(),
            "popularity": random.randint(0, 100),
            "type": "artist",
            "uri": f"spotify:artist:{fake_spotify_url}"
        })
    return {
        "artists": {
            "href": "https://api.spotify.com/v1/search?query=year%3A2023+genre%3Atechno&type=artist&offset=0&limit=50",
            "items": items
        }
    }
