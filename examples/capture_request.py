"""Capture a sample request for the current project."""

from pathlib import Path

from sweeperagent import create_request


def main():
    project_root = Path(__file__).resolve().parents[1]
    path = create_request(project_root, {
        "project": {"name": "sweeper", "zoo_id": None},
        "request": {
            "title": "Add a request capture example",
            "description": "Demonstrate storing a feature request with Sweeper.",
            "directive": "please-hold",
        },
        "context": {
            "interface": "python-example",
            "component": "capture_request",
        },
    })
    print(path)


if __name__ == "__main__":
    main()
