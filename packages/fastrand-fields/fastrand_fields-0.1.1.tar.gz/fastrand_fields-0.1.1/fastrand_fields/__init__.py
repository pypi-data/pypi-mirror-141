import random
import time
import uuid

from fastrand_fields.adjectives import ADJECTIVES
from fastrand_fields.nouns import NOUNS


def fastrand_username(max_length=64, suffix_uuid=True) -> str:
    """Fast random generate for funky username."""
    name = f"{random.choice(ADJECTIVES)}_{random.choice(NOUNS)}"

    if suffix_uuid:
        uid = uuid.uuid5(uuid.NAMESPACE_URL, f"{time.time()}").hex[:8]
        return f"{name}_{uid}"[:max_length]

    return name[:max_length]
