"""Check commit-only scope, complete history, and failure on partial API data."""
from copy import deepcopy
from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from koi_commits import adapt, month_windows, public_commit_days


def repository(visibility, counts, more=False):
    return {
        "repository": {"visibility": visibility},
        "contributions": {
            "nodes": [{"occurredAt": day + "T00:00:00Z", "commitCount": count} for day, count in counts],
            "pageInfo": {"hasNextPage": more},
        },
    }


class CommitKoiTests(unittest.TestCase):
    def collection(self, repositories, total):
        return {"commitContributionsByRepository": repositories, "totalCommitContributions": total}

    def test_only_public_commits_count_and_same_day_repositories_sum(self):
        collection = self.collection([
            repository("PUBLIC", [("2026-01-02", 3)]),
            repository("PUBLIC", [("2026-01-02", 2)]),
            repository("PRIVATE", [("2026-01-02", 99)]),
            repository("INTERNAL", [("2026-01-03", 7)]),
        ], 111)
        self.assertEqual(public_commit_days(collection, date(2026, 1, 1), date(2026, 1, 31)), {date(2026, 1, 2): 5})

    def test_truncation_or_mismatched_totals_fail(self):
        for collection in [
            self.collection([repository("PUBLIC", [], more=True)], 0),
            self.collection([], 1),
        ]:
            with self.assertRaises(ValueError):
                public_commit_days(collection, date(2026, 1, 1), date(2026, 1, 31))

    def test_duplicate_out_of_range_or_negative_days_fail(self):
        for counts in [
            [("2026-01-02", 1), ("2026-01-02", 1)],
            [("2025-12-31", 1)],
            [("2026-01-02", -1)],
        ]:
            with self.assertRaises(ValueError):
                public_commit_days(self.collection([repository("PUBLIC", counts)], 2), date(2026, 1, 1), date(2026, 1, 31))

    def test_month_windows_cover_leap_day_and_partial_months(self):
        self.assertEqual(list(month_windows(date(2024, 2, 28), date(2024, 3, 2))), [
            (date(2024, 2, 28), date(2024, 2, 29)), (date(2024, 3, 1), date(2024, 3, 2)),
        ])

    def snapshot(self):
        return {"schema_version": 3, "account_id": 1, "repositories": [], "language_colors": {},
                "contribution_history": {"observed_on": "2026-02-02", "days": [{"date": "2026-02-02", "contribution_count": 999}]}}

    def test_adapter_replaces_mixed_activity_fills_zeros_and_preserves_identity(self):
        snapshot = self.snapshot()
        original = deepcopy(snapshot)
        def query(text, variables):
            if "createdAt" in text:
                return {"user": {"databaseId": 1, "createdAt": "2026-01-31T12:00:00Z"}}
            day = variables["from"][:10]
            return {"user": {"contributionsCollection": self.collection([repository("PUBLIC", [(day, 2)])], 2)}}
        result, summary = adapt(snapshot, "example", query, today=date(2026, 2, 3))
        self.assertEqual(snapshot, original)
        self.assertEqual(result["contribution_history"]["days"], [
            {"date": "2026-01-31", "contribution_count": 2},
            {"date": "2026-02-01", "contribution_count": 2},
            {"date": "2026-02-02", "contribution_count": 0},
        ])
        self.assertEqual(summary["total_commits"], 4)
        self.assertGreater(summary["growth_fraction"], 0)

    def test_wrong_account_or_incomplete_day_fails(self):
        def query(text, variables):
            return {"user": {"databaseId": 2, "createdAt": "2026-01-31T12:00:00Z"}}
        with self.assertRaises(ValueError):
            adapt(self.snapshot(), "example", query, today=date(2026, 2, 3))
        def correct_account(text, variables):
            return {"user": {"databaseId": 1, "createdAt": "2026-01-31T12:00:00Z"}}
        with self.assertRaises(ValueError):
            adapt(self.snapshot(), "example", correct_account, today=date(2026, 2, 2))

    def test_new_account_can_have_no_complete_days(self):
        snapshot = self.snapshot()
        def query(text, variables):
            self.assertIn("createdAt", text)
            return {"user": {"databaseId": 1, "createdAt": "2026-02-03T00:00:00Z"}}
        result, summary = adapt(snapshot, "example", query, today=date(2026, 2, 3))
        self.assertEqual(result["contribution_history"]["days"], [])
        self.assertEqual(summary["total_commits"], 0)


if __name__ == "__main__":
    unittest.main()
