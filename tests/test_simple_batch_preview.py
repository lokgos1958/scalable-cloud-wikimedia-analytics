import json
import os
import tempfile
import unittest
from pathlib import Path

from src.batch.simple_batch_preview import build_preview_views


class SimpleBatchPreviewTests(unittest.TestCase):
    def write_sample_file(self, records):
        handle = tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".jsonl")
        try:
            for record in records:
                handle.write(json.dumps(record))
                handle.write("\n")
        finally:
            handle.close()
        self.addCleanup(lambda: os.remove(handle.name) if os.path.exists(handle.name) else None)
        return handle.name

    def test_batch_preview_writes_expected_views(self):
        input_path = self.write_sample_file(
            [
                {
                    "wiki": "enwiki",
                    "title": "Python",
                    "timestamp": 1767225600,
                    "bot": False,
                },
                {
                    "wiki": "enwiki",
                    "title": "Python",
                    "timestamp": 1767229200,
                    "bot": True,
                },
                {
                    "wiki": "dewiki",
                    "title": "Berlin",
                    "timestamp": 1767229200,
                    "bot": False,
                },
            ]
        )
        with tempfile.TemporaryDirectory() as folder:
            output_dir = Path(folder)
            build_preview_views(input_path, output_dir)

            top_pages_file = output_dir / "top_pages" / "part-00000.jsonl"
            bot_summary_file = output_dir / "bot_summary" / "part-00000.jsonl"

            top_pages = [json.loads(line) for line in top_pages_file.read_text(encoding="utf-8").splitlines()]
            bot_summary = [json.loads(line) for line in bot_summary_file.read_text(encoding="utf-8").splitlines()]

            self.assertEqual(top_pages[0], {"wiki": "enwiki", "title": "Python", "edit_count": 2})
            self.assertEqual(bot_summary, [{"bot": False, "edit_count": 2}, {"bot": True, "edit_count": 1}])
            self.assertTrue((output_dir / "language_volume" / "part-00000.jsonl").exists())
            self.assertTrue((output_dir / "hourly_volume" / "part-00000.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
