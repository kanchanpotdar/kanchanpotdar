# Maintaining the profile

The profile combines the Koi Research Lab identity with an AI Systems Studio layout. The palette uses deep indigo `#171B2D` / `#202C49`, cream `#F4EBDD`, muted gold `#D9B77A`, and aqua `#82B9C4`. All SVG illustrations are self-contained, use system fonts, and keep contrast high enough for GitHub's light and dark pages. Native Markdown carries the longer explanations and links.

## Content and artwork

Edit `scripts/profile_content.json` to update the hero, three-stop experience timeline, five featured cards, or **Currently exploring** topics. Then run:

```sh
python3 scripts/render_profile.py
```

The standard-library renderer regenerates `assets/koi-lab/banner.svg`, `experience.svg`, `achievements.svg`, their three `-mobile.svg` variants, and the five project cards. It also replaces only the marked project-card and research-notebook blocks in `README.md`. Review the native Markdown project explanations whenever a result or status changes; the renderer does not rewrite those explanations. Keep claims tied to their owning repositories and name the split, metric, denominator, and prototype status where relevant.

The achievement strip is illustrative. Update the native text and alternative text if the personal details change. Avoid adding external image services or animated effects to the primary content.

## Layout and accessibility

The hero, timeline, and achievements strip use `<picture>` with 420px mobile variants; the pond uses `width="100%"`. Cards use nominal `width="420"` and wrap from two columns to one. GitHub scales images on narrow screens. Keep SVG text short and place important qualifications in Markdown, where visitors can read, select, and enlarge them. Every decorative or information-bearing SVG has a title and description; README image alternatives summarize its content. The contribution arcade is secondary and remains inside a disclosure.

Check the rendered README on a wide screen and a phone-width viewport, in both GitHub themes. Inspect text clipping, tap targets, image fallbacks, color contrast, and heading navigation. Parse the SVG files, run the README link checker, and inspect the diff before publishing.

## Automation boundaries

The koi and contribution arcade run through separate existing GitHub Actions workflows. Do not change their schedules, permissions, output paths, or rendering scripts for profile layout edits. The koi workflow writes `koi/pond.gif`, `koi/pond.png`, and `koi/stats.json`; the arcade workflow writes SVGs to the `output` branch. See [commit-koi.md](commit-koi.md) for the koi growth rules. Run `python3 -m unittest discover -s tests -v` after any koi-related change.

## Evidence notes

- The Nyishi card uses the public BTP report's final held-out test CER on 683 clips. Do not mix that with validation CER.
- VoiceEnterprise's 85.09% is document Recall@5 on 178 eligible development questions over a 10,000-document subset. It is not answer-quality or production performance.
- The Financial Research Agent repository currently documents manual verification and no automated test suite. Do not add a test-count claim without a matching test record.
- The OpenAQ card describes the implemented pipeline; its own repository holds run and test details.
- The hydrogen SMR card describes a research reproduction at 853 K and 120 mL/min. Its validation table compares model outputs with values read from a published figure; do not present it as full experimental agreement or plant performance.
- The experience, sports, creative, leadership, and competition details are owner-supplied background. Keep organization names and achievements current.
