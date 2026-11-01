# My commit koi

My gold koi grows with cumulative **GitHub-recognized public commit
contributions**, from account creation through the last complete UTC day. It is
drawn by [Git Koi v1.0.2](https://github.com/yalongwastaken/git-koi/tree/v1.0.2).
[Latest measurements](../koi/stats.json) record the date range and commit total.

## What feeds it

- Public commits credited to `kanchanpotdar` by GitHub's contribution system.
- GitHub's normal eligibility rules apply: an account-associated author email,
  a standalone repository, and its default branch or qualifying `gh-pages`
  branch. This is not a count of every commit on every branch.
- Issues, pull requests, reviews, repository creation, and other non-commit
  contributions do **not** increase size. Private/internal repository commits
  and anonymous private contribution counts are excluded.
- Automatic image updates are authored and committed by `github-actions[bot]`,
  with no personal co-author, so they do not feed my fish. The existing arcade
  workflow remains independent.

Git Koi's standard collector uses the broader contribution calendar, including
activity besides commits. The small `scripts/koi_commits.py` adapter replaces
that calendar with daily public commit counts; the upstream identity, language
data, renderer, animation, and growth formula stay intact. Commit counts also
drive the koi's streaks and daily behavior. Language pigments still reflect
eligible public, non-fork repository primary languages, rather than lines of code.

## Growth and movement

Growth is cumulative rather than a rolling-year score. Its growth fraction is
`ln(1 + min(commits, 100000) / 50) / ln(2001)`: early commits have more visible
effect, and later growth slows. The upstream visual milestones now mean commits:

| Commits | Development |
| ---: | --- |
| 500 | Full-strength language colors |
| 1,500 | Young head, eyes, body width, and fins finish developing |
| 12,750 | Adult anatomy; further growth lengthens the body, fins, and tail |
| 100,000 | Maximum size |

The image canvas stays 512 × 512 pixels, displayed at 256 × 256 in the README;
the **fish inside it** grows. Pixel rounding means every individual commit may
not create a visible size change. Inactivity does not shrink it, although
movement slows after 14 quiet days and enters deep rest after 60. GitHub can
revise older counts (for example after attribution changes or repositories
becoming private/deleted), so corrected public history can reduce its size.

## Automatic updates

`.github/workflows/koi.yml` runs daily at **00:43 UTC / 06:13 IST**, on relevant
code/workflow changes, and manually from **Actions → Grow commit koi → Run
workflow**. Schedules can be delayed by GitHub, and contributions may take time
to appear. The current UTC day is deliberately excluded.

The workflow uses only the repository's built-in `GITHUB_TOKEN`; no personal
token or additional secret is required. Read access is the default, with
`contents: write` limited to the publishing job. Actions are pinned to commit
SHAs. It never publishes activity snapshots or private repository details.

Monthly queries avoid daily-connection pagination limits. The adapter verifies
the fetched counts against GitHub's reported commit total before filtering
private/internal repositories. Truncated connections or a mismatch (including
more than 100 active repositories in a month) fail the run and retain the
previous published images rather than silently undercount. The bot commits
only changed GIF, PNG, and public summary files, then rebases on current `main`
before pushing. Image-update commits do not retrigger this workflow.

If GitHub disables the schedule after a long inactive period, re-enable it in
the repository's Actions tab and run it manually once.

## Verification and attribution

Run `python3 -m unittest discover -s tests -v` to check public-only scope,
complete dates, leap years, account identity, and incomplete-response handling.
GitHub renders the committed looping GIF through a standard README `<img>`;
the animation needs no JavaScript or external image service.

Git Koi is Copyright (c) 2026 Anthony Yalong and is
[MIT licensed](https://github.com/yalongwastaken/git-koi/blob/v1.0.2/LICENSE).
This integration uses its published Action and unmodified release renderer;
upstream source code is not vendored here.

References: [upstream setup](https://github.com/yalongwastaken/git-koi/blob/v1.0.2/docs/getting-started.md),
[GitHub contribution criteria](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference).
