#!/usr/bin/env python3
"""Smoke tests for discussion dashboard aggregation."""

from __future__ import annotations

import unittest
from pathlib import Path

import discussion_dashboard


class DiscussionDashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = discussion_dashboard.load_minutes(Path("docs/data/discussion-minutes.mock.json"))

    def test_summary_metrics(self) -> None:
        summary = discussion_dashboard.metrics(self.data)
        self.assertEqual(summary["discussion_minutes"], 94)
        self.assertEqual(summary["contributions"], 22)
        self.assertEqual(summary["active_topics"], 9)
        self.assertEqual(summary["low_engagement_topics"], 2)
        self.assertEqual(summary["unresolved_questions"], 3)
        self.assertEqual(summary["decisions_made"], 2)

    def test_topic_counts_and_stance_distribution(self) -> None:
        topics = {topic["id"]: topic for topic in discussion_dashboard.topic_summaries(self.data)}
        self.assertEqual(topics["foundation-models"]["count"], 7)
        self.assertEqual(topics["remote-sensing"]["count"], 2)

        benchmark_stances = discussion_dashboard.stance_distribution_for_topic(self.data, "benchmarks")
        self.assertEqual(benchmark_stances["agree"], 2)
        self.assertEqual(benchmark_stances["disagree"], 2)
        self.assertEqual(benchmark_stances["neutral"], 2)

    def test_low_engagement_includes_explicit_status(self) -> None:
        low_topics = {topic["id"] for topic in discussion_dashboard.low_engagement_topics(self.data)}
        self.assertIn("remote-sensing", low_topics)
        self.assertIn("agent-governance", low_topics)


if __name__ == "__main__":
    unittest.main()
