import json
import sqlite3
from pathlib import Path
from uuid import uuid4

from .models import RouteDecision
from .security import redact_basic_pii


class AuditStore:
    def __init__(self, database: str | Path = ":memory:") -> None:
        self.connection = sqlite3.connect(str(database))
        self.connection.execute(
            """CREATE TABLE IF NOT EXISTS decisions (
            trace_id TEXT PRIMARY KEY, request_text TEXT NOT NULL,
            route_json TEXT NOT NULL, status TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP)"""
        )

    def record(self, request_text: str, route: RouteDecision, status: str = "pending_review") -> str:
        trace_id = str(uuid4())
        self.connection.execute(
            "INSERT INTO decisions(trace_id, request_text, route_json, status) VALUES (?, ?, ?, ?)",
            (trace_id, redact_basic_pii(request_text), json.dumps(route.as_dict()), status),
        )
        self.connection.commit()
        return trace_id

    def get(self, trace_id: str) -> dict | None:
        row = self.connection.execute(
            "SELECT trace_id, request_text, route_json, status FROM decisions WHERE trace_id = ?",
            (trace_id,),
        ).fetchone()
        if not row:
            return None
        return {"trace_id": row[0], "request_text": row[1], "route": json.loads(row[2]), "status": row[3]}
