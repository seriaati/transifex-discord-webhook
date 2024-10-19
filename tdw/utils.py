from __future__ import annotations

from typing import TYPE_CHECKING, Any

import git
from fastapi import status

if TYPE_CHECKING:
    import aiohttp


def get_repo_version() -> str:
    repo = git.Repo()
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    return tags[-1].name


async def send_webhook(session: aiohttp.ClientSession, url: str, *, payload: dict[str, Any]) -> bool:
    async with session.post(url, json=payload) as response:
        return response.status == status.HTTP_204_NO_CONTENT
