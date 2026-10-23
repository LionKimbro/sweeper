import json
from datetime import datetime
from pathlib import Path
import tempfile
import unittest

from sweeperagent import create_request, make_request


class RequestTests(unittest.TestCase):
    def test_create_request_writes_versioned_json(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            path = create_request(root, {
                "project": {"name": "sample", "zoo_id": None},
                "request": {
                    "title": "Add export",
                    "description": "Export the selected item.",
                    "directive": "go-ahead",
                },
                "context": {"interface": "tkinter", "component": "editor"},
            })

            record = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(path.parent, root / "db" / "sweep-requests")
            self.assertEqual(path.name, f"{record['request_id']}.json")
            self.assertEqual(record["schema_version"], 1)
            self.assertEqual(record["request"]["directive"], "go-ahead")
            self.assertEqual(record["execution"]["status"], "pending")
            self.assertEqual(record["context"]["notes"], "")
            self.assertIsNotNone(datetime.fromisoformat(record["created_at"]).tzinfo)

    def test_make_request_rejects_unknown_directive(self):
        with self.assertRaises(ValueError):
            make_request({
                "request": {
                    "title": "Add export",
                    "description": "Export the selected item.",
                    "directive": "maybe",
                },
            })


if __name__ == "__main__":
    unittest.main()
