# Keeping this profile useful

The profile uses the **Koi Research Lab** direction: blue project cards, a gold
accent, warm cream text, and a serif nameplate. It emphasizes AI engineering and
research. The banner and cards live in `assets/koi-lab/`; the previous artwork
remains in `assets/` as an archive.

## Palette

| Role | Color |
| --- | --- |
| Ink — banner background | `#1F1F28` |
| Deep blue — project cards | `#223249` |
| Gold — accent and card highlights | `#E6C384` |
| Warm cream — primary artwork text | `#DCD7BA` |
| Soft cream — secondary artwork text | `#C8C4AD` |
| Blue — existing animated pond | `#1E5AA8` |

The palette is inspired by [Kanagawa](https://github.com/rebelot/kanagawa.nvim).
Cards have a 12px corner radius at their nominal 420px display width. The banner
and card artwork use fixed colors; native README text follows the visitor's
GitHub light/dark theme. The existing animated pond keeps its blue background.

## Updating the cards

Edit `scripts/profile_content.json`, then run:

```sh
python3 scripts/render_profile.py
```

The standard-library generator writes the banner, four SVG cards, accessible
image labels, and the **Project notes & current status** disclosure from the same
source. It replaces only the marked project block in `README.md`. It performs no
network requests and never changes the koi or activity workflows.

Each card links directly to its public repository. Fixed 420px image widths let
two cards fit a desktop profile while naturally wrapping into full-size cards
on narrower screens. Longer descriptions and status qualifications remain in
native Markdown inside the disclosure. Keep that text, image labels, and public
repository status consistent when a project advances.

## Content updates

- Use **Current work** for a small number of active projects. Describe the
  problem, contribution, and current stage; replace stage statements when work
  advances. The BTP stage is based on its public README checked on 1 November 2026.
- BeyondBot is labelled **Published prototype**, with partial ledger coverage
  stated on its card and in the notes. Preserve that qualification if adding
  evaluation numbers.
- **Selected builds** keeps older work discoverable without presenting every
  repository as active. Use project links and specific technical descriptions.
- Describe prototypes by their implemented capabilities; add benchmark claims
  only when the linked repository provides reproducible evidence.
- Education, ISI research, aquatics, competition, and TFPS details were retained
  from the existing profile. Update the academic year and leadership role when
  they change.

The koi and contribution arcade retain their independent daily workflows. The
arcade sits inside a disclosure section so projects stay prominent. See
[commit-koi.md](commit-koi.md) for the growth rules and update process.
