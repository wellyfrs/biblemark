import requests

from biblemark.config.cache import get_cache
from config import Config

cache = get_cache()


@cache.cached(timeout=3600, key_prefix="versions")
def fetch_versions(ids: [str]) -> dict:
    return request_api_bible(f"/v1/bibles?ids={','.join(ids)}")


def fetch_books(version_id: str) -> dict:
    return request_api_bible(f"/v1/bibles/{version_id}/books")


def fetch_chapters(version_id: str, book_id: str) -> dict:
    return request_api_bible(f"/v1/bibles/{version_id}/books/{book_id}/chapters")


def fetch_chapter(version_id: str, chapter_id: str) -> dict:
    return request_api_bible(f"/v1/bibles/{version_id}/chapters/{chapter_id}?include-verse-spans=true")


def fetch_passages(version_id: str, passage_id: str) -> dict:
    return request_api_bible(f"/v1/bibles/{version_id}/passages/{passage_id}")


def request_api_bible(url: str) -> dict:
    url = f"{Config.API_BIBLE_BASE_URL}{url}"
    cached_data = cache.get(url)

    if cached_data:
        return cached_data
    else:
        response = requests.get(url, headers={"api-key": Config.API_BIBLE_APP_KEY}, timeout=5)
        response.raise_for_status()

        data = response.json()
        cache.set(url, data)

        return data
