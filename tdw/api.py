from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

import aiofiles
import aiohttp
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from tortoise import Tortoise

from tdw import embeds
from tdw.models import Webhook
from tdw.utils import send_webhook

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.session = aiohttp.ClientSession()
    await Tortoise.init(db_url="sqlite://tdw.db", modules={"models": ["tdw.models"]})
    await Tortoise.generate_schemas()
    yield
    await app.state.session.close()
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root() -> HTMLResponse:
    async with aiofiles.open("tdw/index.html", encoding="utf-8") as f:
        return HTMLResponse(content=await f.read(), status_code=status.HTTP_200_OK)


@app.post("/webhook")
async def create_webhook(data: dict[str, Any]) -> JSONResponse:
    url = data.get("url")
    if url is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL is required")

    webhook = await Webhook.get_or_none(url=url)
    if webhook is not None:
        return JSONResponse(content={"uuid": str(webhook.id)}, status_code=status.HTTP_200_OK)

    webhook = await Webhook.create(url=url)
    return JSONResponse(content={"uuid": str(webhook.id)}, status_code=status.HTTP_201_CREATED)


@app.post("/webhook/{webhook_id}")
async def handle_webhook(webhook_id: str, payload: dict[str, Any]) -> JSONResponse:
    webhook = await Webhook.get_or_none(id=webhook_id)
    if webhook is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook not found")

    event = payload.pop("event")
    del payload["resource"]

    match event:
        case "translation_completed":
            embed = embeds.translation_completed(**payload)
        case "review_completed":
            embed = embeds.review_completed(**payload)
        case "proofread_completed":
            embed = embeds.proofread_completed(**payload)
        case "fillup_completed":
            embed = embeds.fillup_completed(**payload)
        case "translation_completed_updated":
            embed = embeds.translation_completed_updated(**payload)
        case _:
            logger.warning(f"Unrecognized event: {event}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unrecognized event")

    success = await send_webhook(
        app.state.session,
        webhook.url,
        payload={"embeds": [embed], "username": "Transifex", "avatar_url": "https://iili.io/22St8xa.png"},
    )
    if not success:
        await webhook.delete()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to send webhook")

    return JSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)
