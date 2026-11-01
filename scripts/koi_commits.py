"""Replace Git Koi's mixed contribution calendar with public commit counts.

The upstream collector still owns identity, languages, and the observation date;
the unmodified upstream renderer consumes the resulting version-3 snapshot.
Requires only Python's standard library and an authenticated GitHub CLI.
"""
import argparse
import calendar
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
import json
import math
from pathlib import Path
import subprocess


ACCOUNT_QUERY = """query($login: String!) {
  user(login: $login) { databaseId createdAt }
}"""
COMMITS_QUERY = """query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      commitContributionsByRepository(maxRepositories: 100) {
        repository { visibility }
        contributions(first: 100) {
          nodes { occurredAt commitCount }
          pageInfo { hasNextPage }
        }
      }
    }
  }
}"""


def graphql(query, variables):
    result = subprocess.run(
        ["gh", "api", "graphql", "--input", "-"],
        input=json.dumps({"query": query, "variables": variables}),
        capture_output=True, text=True, check=True, timeout=120,
    )
    response = json.loads(result.stdout)
    if response.get("errors"):
        raise ValueError("GitHub GraphQL errors: " + json.dumps(response["errors"]))
    return response["data"]


def month_windows(start, end):
    """Keep each repository's connection below 100 daily contribution nodes."""
    while start <= end:
        last = date(start.year, start.month, calendar.monthrange(start.year, start.month)[1])
        stop = min(last, end)
        yield start, stop
        start = stop + timedelta(days=1)


def public_commit_days(collection, start, end):
    """Reject incomplete/truncated responses rather than silently shrink the koi."""
    daily = {}
    all_visible_commits = 0
    for repository in collection["commitContributionsByRepository"]:
        connection = repository["contributions"]
        if connection["pageInfo"]["hasNextPage"]:
            raise ValueError("Commit day connection was truncated; keeping the previous koi")
        seen = set()
        for node in connection["nodes"]:
            day = datetime.fromisoformat(node["occurredAt"].replace("Z", "+00:00")).astimezone(timezone.utc).date()
            count = node["commitCount"]
            if type(count) is not int or count < 0:
                raise ValueError("Invalid commit count")
            if not start <= day <= end or day in seen:
                raise ValueError("Out-of-range or repeated commit day")
            seen.add(day)
            all_visible_commits += count
            if repository["repository"]["visibility"] == "PUBLIC":
                daily[day] = daily.get(day, 0) + count
    if all_visible_commits != collection["totalCommitContributions"]:
        raise ValueError("Commit totals disagree (possibly over 100 repositories in a month); keeping the previous koi")
    return daily


def adapt(snapshot, login, query=graphql, today=None):
    today = today or datetime.now(timezone.utc).date()
    user = query(ACCOUNT_QUERY, {"login": login})["user"]
    if not user or user["databaseId"] != snapshot["account_id"]:
        raise ValueError("Account does not match the upstream snapshot")
    if snapshot["schema_version"] != 3:
        raise ValueError("Expected Git Koi snapshot schema version 3")
    start = date.fromisoformat(user["createdAt"][:10])
    end = date.fromisoformat(snapshot["contribution_history"]["observed_on"])
    if end >= today or end < start - timedelta(days=1):
        raise ValueError("Observation must cover complete days since account creation")
    counts = {}
    for first, last in month_windows(start, end):
        data = query(COMMITS_QUERY, {
            "login": login,
            "from": f"{first}T00:00:00Z",
            "to": f"{last}T23:59:59Z",
        })
        counts.update(public_commit_days(data["user"]["contributionsCollection"], first, last))
    result = deepcopy(snapshot)
    days = []
    current = start
    while current <= end:
        days.append({"date": current.isoformat(), "contribution_count": counts.get(current, 0)})
        current += timedelta(days=1)
    result["contribution_history"] = {"observed_on": end.isoformat(), "days": days}
    total = sum(counts.values())
    summary = {
        "login": login,
        "metric": "GitHub-recognized public commit contributions",
        "since": start.isoformat(),
        "through": end.isoformat(),
        "total_commits": total,
        "growth_fraction": round(math.log1p(min(total, 100_000) / 50) / math.log1p(100_000 / 50), 6),
        "max_growth_commits": 100_000,
        "renderer": "yalongwastaken/git-koi v1.0.2",
    }
    return result, summary


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("login")
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    try:
        result, summary = adapt(json.loads(args.snapshot.read_text()), args.login)
        write_json(args.output, result)
        write_json(args.summary, summary)
    except (ValueError, KeyError, subprocess.SubprocessError) as error:
        parser.exit(1, f"Commit collection failed: {error}\n")
    print(f"{summary['total_commits']} public commit contributions through {summary['through']}")


if __name__ == "__main__":
    main()
