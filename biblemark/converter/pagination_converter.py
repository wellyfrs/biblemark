from math import ceil
from typing import List


def build_paginated_response(size: int, total_elements: int, number: int, content: List[dict]) -> dict:
    return {
        "page": {
            "size": size,
            "totalElements": total_elements,
            "totalPages": max(1, ceil(total_elements / size)),
            "number": number,
        },
        "content": content
    }