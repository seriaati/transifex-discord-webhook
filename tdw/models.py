from __future__ import annotations

from tortoise import Model, fields


class Webhook(Model):
    id = fields.UUIDField(pk=True)
    url = fields.TextField()
