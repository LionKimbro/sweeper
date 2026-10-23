# Sweeper

Sweeper captures software improvement requests so they can be picked up by an
AI coding agent later. Its first slice is a small Python library that writes
each request as a versioned JSON file in the owning project's
`db/sweep-requests/` directory.

## Use

```python
from pathlib import Path
from sweeperagent import create_request

path = create_request(Path("/path/to/project"), {
    "project": {"name": "my-app", "zoo_id": None},
    "request": {
        "title": "Add export to JSON",
        "description": "Export the selected entry as JSON.",
        "directive": "go-ahead",
    },
    "context": {"interface": "tkinter", "component": "entry-editor"},
})
```

The directive may be `go-ahead`, `please-investigate`, or `please-hold`.
`create_request()` returns the created file path. See
[`docs/manual/capture.md`](docs/manual/capture.md) for installation, field
details, and a reusable integration prompt. The request format is described in
[`docs/raw/0002__request-format-v1.json`](docs/raw/0002__request-format-v1.json).

Run `python examples/capture_request.py` to write a sample request into the
current checkout.
