"""Render the Koi Research Lab banner, cards, and README project block.

Edit profile_content.json, then run this script with Python 3.11+. It uses only
the standard library and does not access GitHub, collect activity, or draw the koi.
"""
import json
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
START = "<!-- PROJECT_CARDS:START -->"
END = "<!-- PROJECT_CARDS:END -->"


def text(x, y, content, size, color, *, family="Arial, Helvetica, sans-serif", weight=400, spacing=None):
    tracking = f' letter-spacing="{spacing}"' if spacing is not None else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}"{tracking}>{escape(content)}</text>')


def svg_document(width, height, title, description, drawing):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
            f'<title id="title">{escape(title)}</title>\n'
            f'<desc id="desc">{escape(description)}</desc>\n'
            + "\n".join(drawing) + "\n</svg>\n")


def icon(kind, color):
    shapes = {
        "speech": '<path d="M2 15v6m6-14v22m6-29v36m6-26v16m6-22v28m6-18v8"/>',
        "voice": '<rect x="11" y="1" width="13" height="23" rx="6.5"/><path d="M5 18v2a12.5 12.5 0 0 0 25 0v-2M17.5 32v6M10 38h15"/>',
        "book": '<path d="M17 7C9 1 1 3 1 3v29s8-2 16 4c8-6 16-4 16-4V3s-8-2-16 4Zm0 0v29"/>',
        "calculator": '<rect x="3" y="0" width="28" height="37" rx="4"/><path d="M8 7h18M8 15h3m7 0h3M8 23h3m7 0h3M8 31h3m7 0h3"/>',
    }
    return (f'<g transform="translate(34 24)" fill="none" stroke="{color}" '
            f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">{shapes[kind]}</g>')


def render_card(project, palette, radius):
    description = " ".join(project["summary"]) + " " + project["stage"]
    drawing = [
        f'<defs><clipPath id="card"><rect x="1" y="1" width="838" height="358" rx="{radius}"/></clipPath></defs>',
        f'<rect x="1" y="1" width="838" height="358" rx="{radius}" fill="{palette["panel"]}" stroke="{palette["line"]}" stroke-width="2"/>',
        f'<rect width="840" height="6" fill="{palette["accent"]}" clip-path="url(#card)"/>',
        icon(project["icon"], palette["accent"]),
        text(84, 52, project["category"], 24, palette["accent"], spacing=2),
        text(34, 119, project["title"], 40, palette["text"], weight=600),
        text(34, 175, project["summary"][0], 30, palette["muted"]),
        text(34, 216, project["summary"][1], 30, palette["muted"]),
        text(34, 274, project["stage"], 28, palette["text"]),
        text(34, 326, project["stack"], 26, palette["accent"], spacing=1),
    ]
    return svg_document(840, 360, project["title"], description, drawing)


def render_banner(content):
    p = content["palette"]
    drawing = [
        f'<rect width="1200" height="300" rx="18" fill="{p["background"]}"/>',
        text(40, 44, content["education"], 18, p["muted"], spacing=2.4),
        text(38, 129, content["name"], 72, p["text"], family="Georgia, Times New Roman, serif"),
        text(40, 177, content["focus"], 27, p["muted"]),
        f'<path d="M40 213H1160" stroke="{p["line"]}" stroke-width="1.5"/>',
        text(40, 258, content["tagline"], 22, p["text"]),
        f'<g opacity=".75">{text(1045, 143, "水", 112, p["accent"], family="serif")}</g>',
        text(997, 187, "KOI RESEARCH LAB", 15, p["accent"], spacing=1.6),
        f'<g fill="none" stroke="{p["wave"]}" stroke-width="2" opacity=".55"><path d="M928 240q28-17 56 0t56 0t56 0t56 0"/><path d="M928 255q28-17 56 0t56 0t56 0t56 0"/></g>',
    ]
    return svg_document(1200, 300, content["name"] + " — Koi Research Lab",
                        "A Kanagawa-inspired research profile in deep blue, warm cream, and gold.", drawing)


def project_block(projects):
    # Fixed-size images wrap naturally: two 420px cards fit the desktop profile;
    # GitHub's max-width rule makes each card fill a narrower mobile container.
    lines = [START, '<p align="center">']
    for project in projects:
        alt = f'{project["title"]} — {project["category"].lower()}. {project["stage"]}.'
        lines.append(f'<a href="{escape(project["url"], quote=True)}"><img src="./assets/koi-lab/{project["id"]}.svg" width="420" alt="{escape(alt, quote=True)}" /></a>')
    lines.extend(['</p>', '', '<details>', '<summary><b>Project notes &amp; current status</b></summary>', ''])
    for project in projects:
        lines.extend([f'### [{project["title"]}]({project["url"]})', '', project["notes"], '',
                      "**Current stage:** " + project["status_detail"], ''])
    lines.extend(['</details>', END])
    return "\n".join(lines)


def main():
    content = json.loads((ROOT / "scripts/profile_content.json").read_text())
    assets = ROOT / "assets/koi-lab"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "banner.svg").write_text(render_banner(content))
    for project in content["projects"]:
        (assets / (project["id"] + ".svg")).write_text(
            render_card(project, content["palette"], content["card_radius_at_420px"] * 2))
    readme_path = ROOT / "README.md"
    readme = readme_path.read_text()
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError("README must contain one pair of PROJECT_CARDS markers")
    before, remainder = readme.split(START, 1)
    _, after = remainder.split(END, 1)
    readme_path.write_text(before + project_block(content["projects"]) + after)
    print(f'Rendered banner and {len(content["projects"])} project cards; updated README block')


if __name__ == "__main__":
    main()
