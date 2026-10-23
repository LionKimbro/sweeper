"""Build and store one Sweeper request as a JSON file."""

from __future__ import annotations

from datetime import datetime
import json
import os
from pathlib import Path
import tempfile
from uuid import uuid4

DIRECTIVES = {"go-ahead", "please-investigate", "please-hold"}
REQUEST_DIRECTORY = Path("db") / "sweep-requests"


def make_request(request: dict) -> dict:
    """Return a complete version 1 request from its caller-supplied fields.

    ``request`` is a record with ``project`` and ``request`` objects; optional
    ``context`` may supply interface, component, active_item_id, and notes.
    """
    if not isinstance(request, dict):
        raise TypeError("request must be a dictionary")

    project = request.get("project", {})
    request_fields = request.get("request", {})
    context = request.get("context", {})
    if not isinstance(project, dict) or not isinstance(request_fields, dict):
        raise TypeError("project and request must be dictionaries")
    if not isinstance(context, dict):
        raise TypeError("context must be a dictionary")

    title = request_fields.get("title")
    description = request_fields.get("description")
    directive = request_fields.get("directive", "go-ahead")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("request.title must be a non-empty string")
    if not isinstance(description, str) or not description.strip():
        raise ValueError("request.description must be a non-empty string")
    if directive not in DIRECTIVES:
        raise ValueError(f"request.directive must be one of {sorted(DIRECTIVES)}")

    return {
        "schema_version": 1,
        "request_id": str(uuid4()),
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "project": {
            "name": project.get("name"),
            "zoo_id": project.get("zoo_id"),
        },
        "request": {
            "title": title.strip(),
            "description": description.strip(),
            "directive": directive,
        },
        "context": {
            "interface": context.get("interface"),
            "component": context.get("component"),
            "active_item_id": context.get("active_item_id"),
            "notes": context.get("notes", ""),
        },
        "execution": {
            "status": "pending",
            "agent": None,
            "started_at": None,
            "completed_at": None,
        },
    }


def create_request(project_root: str | os.PathLike, request: dict) -> Path:
    """Atomically save a new request under ``<project>/db/sweep-requests``."""
    record = make_request(request)
    directory = Path(project_root) / REQUEST_DIRECTORY
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / f"{record['request_id']}.json"
    encoded = json.dumps(record, ensure_ascii=False, indent=2) + "\n"

    fd, temp_name = tempfile.mkstemp(prefix=".sweeper-", suffix=".tmp", dir=directory)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        # A hard link publishes the complete file and fails rather than
        # replacing an existing request if a UUID collision ever occurs.
        os.link(temp_path, destination)
        try:
            directory_fd = os.open(directory, os.O_RDONLY)
        except OSError:
            directory_fd = None
        if directory_fd is not None:
            try:
                os.fsync(directory_fd)
            except OSError:
                pass
            finally:
                os.close(directory_fd)
    finally:
        temp_path.unlink(missing_ok=True)

    return destination
