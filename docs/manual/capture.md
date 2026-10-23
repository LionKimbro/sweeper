# Capturing requests

Sweeper stores one JSON file per request in `<project-root>/db/sweep-requests/`.
The Python library creates the directory when needed and writes complete files
atomically. The format is documented in
[`../raw/0002__request-format-v1.json`](../raw/0002__request-format-v1.json).

## Python API

Install the package in the application environment (for a local checkout,
run `python -m pip install .`), then call
`sweeperagent.create_request(project_root, request_record)`:

```python
from pathlib import Path
from sweeperagent import create_request

path = create_request(Path("/path/to/project"), {
    "project": {"name": "my-app", "zoo_id": None},
    "request": {
        "title": "Add export to JSON",
        "description": "Export the selected entry as a JSON file.",
        "directive": "go-ahead",
    },
    "context": {
        "interface": "tkinter",
        "component": "entry-editor",
        "active_item_id": "entry-42",
        "notes": "",
    },
})
print(path)
```

The `request` record must have a non-empty title and description. Its directive
defaults to `go-ahead`; allowed values are `go-ahead`, `please-investigate`,
and `please-hold`. `project` and `context` fields may be omitted. The function
returns the path to the new file. It generates the UUID and timezone-aware
creation time, and initializes execution to `pending`.

Run `python examples/capture_request.py` from a checkout to see a complete
example. It writes a sample `please-hold` request into that checkout.

Run the focused tests from a checkout with `run-tests.bat` on Windows, or
`PYTHONPATH=src python -m unittest discover -s tests -v` on macOS or Linux.

## Reusable integration prompt

> Add Sweeper request capture support to this application. Use the `sweeperagent`
> Python package and its `create_request(project_root, request_record)` API.
> Provide a lightweight capture interface with the directives `go-ahead`,
> `please-investigate`, and `please-hold`. Supply the project name and useful
> context such as interface, component, selected item, and notes when available.
> Save requests in the application's project root and keep the normal workflow
> uninterrupted. Do not dispatch or implement requests as part of capture.
