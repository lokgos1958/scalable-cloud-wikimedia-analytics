import unittest

from src.serving.merge_views import merge_top_counts


class MergeTopCountsTests(unittest.TestCase):
    def test_merge_combines_batch_and_speed_counts_for_same_page(self):
        batch_rows = [
            {"wiki": "enwiki", "title": "Python_(programming_language)", "edit_count": 4},
            {"wiki": "dewiki", "title": "Berlin", "edit_count": 2},
        ]
        speed_rows = [
            {"wiki": "enwiki", "title": "Python_(programming_language)", "edit_count": 3},
            {"wiki": "frwiki", "title": "Paris", "edit_count": 5},
        ]

        merged = merge_top_counts(batch_rows, speed_rows, limit=3)

        self.assertEqual(
            merged,
            [
                {
                    "wiki": "enwiki",
                    "title": "Python_(programming_language)",
                    "batch_edit_count": 4,
                    "speed_edit_count": 3,
                    "combined_edit_count": 7,
                },
                {
                    "wiki": "frwiki",
                    "title": "Paris",
                    "batch_edit_count": 0,
                    "speed_edit_count": 5,
                    "combined_edit_count": 5,
                },
                {
                    "wiki": "dewiki",
                    "title": "Berlin",
                    "batch_edit_count": 2,
                    "speed_edit_count": 0,
                    "combined_edit_count": 2,
                },
            ],
        )

    def test_merge_respects_limit(self):
        merged = merge_top_counts(
            batch_rows=[
                {"wiki": "enwiki", "title": "A", "edit_count": 1},
                {"wiki": "enwiki", "title": "B", "edit_count": 2},
            ],
            speed_rows=[
                {"wiki": "enwiki", "title": "C", "edit_count": 3},
            ],
            limit=2,
        )

        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0]["title"], "C")
        self.assertEqual(merged[1]["title"], "B")


if __name__ == "__main__":
    unittest.main()
