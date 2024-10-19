from __future__ import annotations

from typing import Any

__all__ = (
    "fillup_completed",
    "proofread_completed",
    "review_completed",
    "translation_completed",
    "translation_completed_updated",
)


def get_embed(*, title: str, fields: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "title": title,
        "color": 25771,
        "fields": fields,
        "footer": {"text": "Powered by transifex-discord-webhook"},
    }


def translation_completed(*, project: str, translated: int, language: str) -> dict[str, Any]:
    return get_embed(
        title="Translation Completed",
        fields=[
            {"name": "Project", "value": project, "inline": False},
            {"name": "Language", "value": language, "inline": False},
            {"name": "Percentage", "value": f"{translated}%", "inline": False},
        ],
    )


def review_completed(*, project: str, reviewed: int, language: str, is_final: bool) -> dict[str, Any]:
    return get_embed(
        title="Review Completed",
        fields=[
            {"name": "Project", "value": project, "inline": False},
            {"name": "Language", "value": language, "inline": False},
            {"name": "Percentage", "value": f"{reviewed}%", "inline": False},
            {"name": "Final", "value": "Yes" if is_final else "No", "inline": False},
        ],
    )


def proofread_completed(*, project: str, reviewed: int, language: str, is_final: bool) -> dict[str, Any]:
    return get_embed(
        title="Proofread Completed",
        fields=[
            {"name": "Project", "value": project, "inline": False},
            {"name": "Language", "value": language, "inline": False},
            {"name": "Percentage", "value": f"{reviewed}%", "inline": False},
            {"name": "Final", "value": "Yes" if is_final else "No", "inline": False},
        ],
    )


def fillup_completed(*, project: str, translated: int, language: str, translation_memory: int) -> dict[str, Any]:
    return get_embed(
        title="Fillup Completed",
        fields=[
            {"name": "Project", "value": project, "inline": False},
            {"name": "Language", "value": language, "inline": False},
            {"name": "Translation percentage", "value": f"{translated}%", "inline": False},
            {"name": "TM percentage", "value": f"{translation_memory}%", "inline": False},
        ],
    )


def translation_completed_updated(*, project: str, translated: float, language: str) -> dict[str, Any]:
    return get_embed(
        title="Translation Updated",
        fields=[
            {"name": "Project", "value": project, "inline": False},
            {"name": "Language", "value": language, "inline": False},
            {"name": "Percentage", "value": f"{translated}%", "inline": False},
        ],
    )
