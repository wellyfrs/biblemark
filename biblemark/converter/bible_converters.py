def build_chapter_content_response(version_id: str, chapter_content: dict) -> dict:
    return {
        "chapter": {
            "versionId": version_id,
            "bookId": chapter_content["bookId"],
            "chapterId": chapter_content["number"],
            "reference": chapter_content["reference"],
            "content": chapter_content["content"],
        },
        "_links": build_chapter_content_hateoas(version_id, chapter_content)
    }


def build_chapter_content_hateoas(version_id, chapter_content):
    links = {
        "self": {
            "versionId": version_id,
            "bookId": chapter_content["bookId"],
            "chapterId": chapter_content["number"],
            "href": f"/{version_id}/{chapter_content['bookId']}/{chapter_content['number']}",
        },
    }

    if "previous" in chapter_content:
        links["prev"] = {
            "versionId": version_id,
            "bookId": chapter_content["previous"]["bookId"],
            "chapterId": chapter_content["previous"]["number"],
            "href": f"/{version_id}/{chapter_content['previous']['bookId']}/{chapter_content['previous']['number']}",
        }

    if "next" in chapter_content:
        links["next"] = {
            "versionId": version_id,
            "bookId": chapter_content["next"]["bookId"],
            "chapterId": chapter_content["next"]["number"],
            "href": f"/{version_id}/{chapter_content['next']['bookId']}/{chapter_content['next']['number']}",
        }

    return links
