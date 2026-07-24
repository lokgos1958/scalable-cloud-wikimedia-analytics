import json
import os
import tempfile
import unittest

from src.speed.sliding_window_analytics import run_window_replay


class RunWindowReplayTests(unittest.TestCase):
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

    def test_replay_counts_valid_events_and_top_titles(self):
        input_path = self.write_sample_file(
            [
                {"wiki": "enwiki", "title": "Python_(programming_language)", "bot": False, "anon": False, "type": "edit"},
                {"wiki": "enwiki", "title": "Python_(programming_language)", "bot": True, "anon": True, "type": "edit"},
                {"wiki": "dewiki", "title": "Berlin", "bot": False, "anon": True, "type": "new"},
                {"wiki": "enwiki"},
            ]
        )

        summary = run_window_replay(
            input_path=input_path,
            window_seconds=300,
            top_n=2,
            report_every=2,
            emit_progress=False,
        )

        self.assertEqual(summary["processed_events"], 3)
        self.assertEqual(summary["snapshots_emitted"], 2)
        self.assertEqual(summary["final_window_size"], 3)
        self.assertEqual(
            summary["final_top_titles"],
            [("enwiki:Python_(programming_language)", 2), ("dewiki:Berlin", 1)],
        )
        self.assertEqual(summary["final_top_wikis"], [("enwiki", 2), ("dewiki", 1)])
        self.assertEqual(summary["final_top_event_types"], [("edit", 2), ("new", 1)])
        self.assertEqual(summary["final_bot_breakdown"], {"bot_events": 1, "human_events": 2})
        self.assertEqual(summary["final_editor_breakdown"], {"anonymous_events": 2, "logged_in_events": 1})

    def test_replay_handles_files_without_valid_events(self):
        input_path = self.write_sample_file(
            [
                {"wiki": "enwiki"},
                {"title": "Missing wiki"},
                {},
            ]
        )

        summary = run_window_replay(
            input_path=input_path,
            window_seconds=300,
            top_n=3,
            emit_progress=False,
        )

        self.assertEqual(summary["processed_events"], 0)
        self.assertEqual(summary["snapshots_emitted"], 0)
        self.assertEqual(summary["final_window_size"], 0)
        self.assertEqual(summary["final_top_titles"], [])
        self.assertEqual(summary["final_top_wikis"], [])
        self.assertEqual(summary["final_top_event_types"], [])
        self.assertEqual(summary["final_bot_breakdown"], {"bot_events": 0, "human_events": 0})
        self.assertEqual(summary["final_editor_breakdown"], {"anonymous_events": 0, "logged_in_events": 0})


if __name__ == "__main__":
    unittest.main()
