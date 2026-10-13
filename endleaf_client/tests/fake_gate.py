"""In-memory gate for unit tests. Blob in, summary out."""

from __future__ import annotations

import base64
import hashlib
import json
from typing import Any

from endleaf_client.paths import sha256_hex


def artifact_pdf(payload: bytes = b"hello-endleaf") -> bytes:
    return b"%PDF-1.4\n" + payload + b"\n%%EOF\n"


class FakeGate:
    def __init__(self, artifact: bytes | None = None, max_doc_kib: int = 256) -> None:
        self.artifact = artifact if artifact is not None else artifact_pdf()
        digest = sha256_hex(self.artifact)
        self.digest = digest
        self.filename = f"endleaf-document-shell-{digest[:8]}.pdf"
        self.summary = (
            f"ok pages=1 bytes={len(self.artifact)} sha256={digest} "
            f"format=pdf templateId=document-shell kind=document-shell file={self.filename}"
        )
        self.quota: dict[str, Any] = {
            "plan": "free",
            "plan_status": "free",
            "limits": {"jobs_per_day": 50, "per_minute": 5, "max_doc_kib": max_doc_kib},
        }
        self.expires_at = "2026-10-09T00:00:00Z"
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.generation = 0
        self.uploads: list[bytes] = []
        self.tools = [
            {
                "name": "renderDocument",
                "description": "Send a body; Endleaf owns the preamble.",
                "inputSchema": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["outputFormat", "templateId"],
                    "properties": {
                        "outputFormat": {"type": "string"},
                        "templateId": {"type": "string"},
                        "source": {"type": "string"},
                        "source_id": {"type": "string"},
                        "delivery": {"type": "string"},
                    },
                },
            },
            {
                "name": "uploadSource",
                "description": "Store source bytes.",
                "inputSchema": {"type": "object", "properties": {"blob_b64": {"type": "string"}}},
            },
            {
                "name": "getQuota",
                "description": "Return plan.",
                "inputSchema": {"type": "object", "properties": {}},
            },
            {
                "name": "guide",
                "description": "Return one topic.",
                "inputSchema": {"type": "object", "properties": {"topic": {"type": "string"}}},
            },
        ]

    async def list_tools(self) -> list[dict[str, Any]]:
        return list(self.tools)

    async def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        args = dict(arguments or {})
        self.calls.append((name, args))
        if name == "getQuota":
            return _text(json.dumps(self.quota, sort_keys=True))
        if name == "uploadSource":
            raw = args.get("blob_b64")
            if not isinstance(raw, str):
                return _text("blob_b64 must be standard base64 of non-empty bytes\nFix: send blob_b64.", error=True)
            data = base64.b64decode(raw, validate=True)
            self.uploads.append(data)
            payload = {
                "source_id": f"src_{hashlib.sha256(data).hexdigest()[:8]}",
                "sha256": sha256_hex(data),
                "bytes": len(data),
                "expires_at": self.expires_at,
            }
            return _text(json.dumps(payload, sort_keys=True))
        if name == "renderDocument":
            encoded = base64.b64encode(self.artifact).decode("ascii")
            return {
                "content": [
                    {"type": "text", "text": self.summary},
                    {
                        "type": "resource",
                        "resource": {
                            "uri": f"endleaf://result/{self.digest}.pdf",
                            "name": self.filename,
                            "mimeType": "application/pdf",
                            "blob": encoded,
                            "_meta": {"filename": self.filename},
                        },
                    },
                ],
                "isError": False,
            }
        if name == "guide":
            return _text("getting-started")
        return _text(f"unknown tool: {name}", error=True)


def _text(text: str, *, error: bool = False) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": text}], "isError": error}
