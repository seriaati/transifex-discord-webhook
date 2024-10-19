from __future__ import annotations

import uvicorn

from tdw.api import app

if __name__ == "__main__":
    uvicorn.run(app, port=6407)
