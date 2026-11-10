"""Render the profile's SVG artwork and generated README sections.

Edit profile_content.json, then run `python3 scripts/render_profile.py`.
Standard library only; this does not draw the koi or alter either workflow.
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/koi-lab"


def el(tag, **attrs):
    return "<" + tag + " " + " ".join(f'{key.replace("_", "-")}="{escape(str(value), quote=True)}"' for key, value in attrs.items()) + "/>"


def txt(x, y, value, size, color, *, weight=400, family="Arial, Helvetica, sans-serif", spacing=None):
    extra = f' letter-spacing="{spacing}"' if spacing is not None else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}"{extra}>{escape(value)}</text>')


def svg(width, height, title, desc, parts):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
            f'<title id="title">{escape(title)}</title>\n<desc id="desc">{escape(desc)}</desc>\n'
            + "\n".join(parts) + "\n</svg>\n")


def defs(p, name):
    return (f'<defs><linearGradient id="{name}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{p["ink"]}"/><stop offset="1" stop-color="{p["indigo"]}"/>'
            '</linearGradient></defs>')


def banner(c):
    p = c["palette"]
    a = [defs(p, "sea"), el("rect", x=0, y=0, width=1200, height=350, rx=20, fill="url(#sea)"),
         el("path", d="M520 278 C700 215 820 335 1000 266 S1120 235 1200 270", fill="none", stroke=p["indigo_light"], stroke_width=3),
         el("path", d="M520 309 C700 245 840 353 1020 296 S1130 260 1200 300", fill="none", stroke=p["aqua"], stroke_opacity=".36", stroke_width=2),
         el("circle", cx=1040, cy=124, r=66, fill="none", stroke=p["gold"], stroke_width=2, opacity=".65"),
         el("path", d="M1005 124c22-27 51-29 78 0-27 29-56 27-78 0Zm-4 0-20-17v34zM1056 119l19-19", fill="none", stroke=p["gold"], stroke_width=3, stroke_linecap="round", stroke_linejoin="round"),
         txt(48, 55, "KOI RESEARCH LAB  /  AI SYSTEMS STUDIO", 17, p["gold"], weight=700, spacing="2.7"),
         txt(46, 150, c["name"], 78, p["cream"], family="Georgia, Times New Roman, serif"),
         txt(49, 201, c["positioning"], 31, p["cream"], weight=600),
         txt(49, 247, c["affiliation"], 24, p["muted"]),
         txt(49, 285, c["focus"], 19, p["gold"], spacing="1"),
         txt(49, 325, "IBM Research  /  EY GDS  /  University of Manchester", 17, p["muted"]) ]
    return svg(1200, 350, "Kanchan Potdar — AI/ML engineer and researcher", "Koi Research Lab banner with an outlined koi, indigo water, and gold type", a)


def banner_mobile(c):
    p = c["palette"]
    a = [defs(p, "mobile-sea"), el("rect", x=0, y=0, width=420, height=330, rx=18, fill="url(#mobile-sea)"),
         el("circle", cx=350, cy=73, r=34, fill="none", stroke=p["gold"], stroke_width=2),
         el("path", d="M334 73c11-13 24-13 36 0-12 13-25 13-36 0Zm-2 0-11-9v18z", fill="none", stroke=p["gold"], stroke_width=2),
         txt(22, 36, "KOI RESEARCH LAB  /  AI SYSTEMS STUDIO", 10, p["gold"], weight=700, spacing="1"),
         txt(21, 104, c["name"], 39, p["cream"], family="Georgia, Times New Roman, serif"),
         txt(23, 146, c["positioning"], 20, p["cream"], weight=600),
         txt(23, 179, c["affiliation"], 16, p["muted"]),
         el("path", d="M22 208H398", stroke=p["indigo_light"], stroke_width=2),
         txt(23, 240, "Speech AI / Retrieval / Dependable agents", 15, p["gold"]),
         txt(23, 276, "IBM Research  /  EY GDS", 14, p["muted"]),
         txt(23, 301, "University of Manchester", 14, p["muted"])]
    return svg(420, 330, "Kanchan Potdar — AI/ML engineer and researcher", "Mobile Koi Research Lab banner with IIT Kharagpur and research and industry experience", a)


def icon(kind, p):
    paths = {
        "wave": "M0 32c12 0 12-24 24-24s12 48 24 48 12-48 24-48 12 24 24 24",
        "nodes": "M8 18 48 8 83 35 48 60 8 18M48 8v52",
        "branch": "M9 56V10m0 22h53M62 32l-12-12m12 12L50 44M9 56h53",
        "air": "M4 17h59c24 0 24 28 0 28H24m-20 9h48"
    }
    return f'<g transform="translate(42 31)" fill="none" stroke="{p["gold"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="{paths[kind]}"/></g>'


def card(project, p):
    a = [defs(p, "card-bg"), el("rect", x=1, y=1, width=838, height=418, rx=23, fill="url(#card-bg)", stroke=p["indigo_light"], stroke_width=2),
         el("path", d="M31 83H809", stroke=p["indigo_light"], stroke_width=2),
         icon(project["icon"], p),
         txt(150, 58, project["eyebrow"], 20, p["gold"], weight=700, spacing="1.4"),
         txt(37, 145, project["name"], 41, p["cream"], weight=600),
         txt(39, 200, project["description"][0], 28, p["muted"]),
         txt(39, 240, project["description"][1], 28, p["muted"]),
         el("path", d="M38 274H802", stroke=p["indigo_light"], stroke_width=2),
         txt(39, 333, project["result"], 32, p["cream"], weight=600),
         txt(39, 384, project["footnote"], 22, p["gold"])]
    return svg(840, 420, project["name"], project["eyebrow"] + ". " + " ".join(project["description"]) + " " + project["result"] + ". " + project["footnote"], a)


def timeline(c):
    p = c["palette"]
    a = [defs(p, "timeline-bg"), el("rect", x=0, y=0, width=1200, height=185, rx=18, fill="url(#timeline-bg)"),
         txt(35, 39, "EXPERIENCE  /  RESEARCH & INDUSTRY", 18, p["gold"], weight=700, spacing="2"),
         el("path", d="M75 90H1125", stroke=p["indigo_light"], stroke_width=3)]
    for i, item in enumerate(c["experience"]):
        x = 75 + i * 500
        if i == 2:
            x = 1110
        # Right-align the final stop to keep long organization text inside the viewBox.
        anchor = "end" if i == 2 else "start"
        text_x = x if i != 2 else 1122
        a.extend([el("circle", cx=x, cy=90, r=8, fill=p["gold"]),
                  f'<text x="{text_x}" y="129" text-anchor="{anchor}" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="700" fill="{p["cream"]}">{escape(item["organization"])}</text>',
                  f'<text x="{text_x}" y="158" text-anchor="{anchor}" font-family="Arial, Helvetica, sans-serif" font-size="19" fill="{p["muted"]}">{escape(item["work"])}</text>'])
    return svg(1200, 185, "Experience across research and industry", "IBM Research: multilingual LLMs; EY GDS: AI agents and Azure; University of Manchester: PM2.5 calibration", a)


def timeline_mobile(c):
    p = c["palette"]
    a = [defs(p, "timeline-mobile-bg"), el("rect", x=0, y=0, width=420, height=355, rx=18, fill="url(#timeline-mobile-bg)"),
         txt(22, 37, "EXPERIENCE / RESEARCH & INDUSTRY", 14, p["gold"], weight=700, spacing="1"),
         el("path", d="M39 80V300", stroke=p["indigo_light"], stroke_width=3)]
    for i, item in enumerate(c["experience"]):
        y = 91 + i * 100
        a.extend([el("circle", cx=39, cy=y, r=6, fill=p["gold"]),
                  txt(62, y + 4, item["organization"], 17 if i == 2 else 20, p["cream"], weight=700),
                  txt(62, y + 32, item["work"], 17, p["muted"])])
    return svg(420, 355, "Experience across research and industry", "IBM Research: multilingual LLMs; EY GDS: AI agents and Azure; University of Manchester: PM2.5 calibration", a)


def achievements(c):
    p = c["palette"]
    items = [("01", "SWIMMING", "Inter-IIT aquatics gold"),
             ("02", "PHOTOGRAPHY", "Framing stories beyond code"),
             ("03", "ART & LEADERSHIP", "Creative work · TFPS Governor")]
    a = [defs(p, "ach-bg"), el("rect", x=0, y=0, width=1200, height=210, rx=18, fill="url(#ach-bg)"),
         txt(35, 38, "BEYOND THE LAB", 18, p["gold"], weight=700, spacing="2")]
    for i, (num, title, sub) in enumerate(items):
        x = 36 + i * 396
        a.extend([el("rect", x=x, y=62, width=374, height=119, rx=14, fill=p["indigo"], stroke=p["indigo_light"]),
                  txt(x + 20, 102, num, 22, p["gold"], family="Georgia, Times New Roman, serif"),
                  txt(x + 66, 102, title, 20, p["cream"], weight=700, spacing="1"),
                  txt(x + 20, 147, sub, 20, p["muted"])])
    return svg(1200, 210, "Beyond the lab", "Swimming, photography, art, and TFPS leadership", a)


def achievements_mobile(c):
    p = c["palette"]
    items = [("01", "SWIMMING", "Inter-IIT aquatics gold"),
             ("02", "PHOTOGRAPHY", "Framing stories beyond code"),
             ("03", "ART & LEADERSHIP", "Creative work · TFPS Governor")]
    a = [defs(p, "ach-mobile-bg"), el("rect", x=0, y=0, width=420, height=365, rx=18, fill="url(#ach-mobile-bg)"),
         txt(22, 36, "BEYOND THE LAB", 15, p["gold"], weight=700, spacing="1.5")]
    for i, (num, title, sub) in enumerate(items):
        y = 54 + i * 100
        a.extend([el("rect", x=20, y=y, width=380, height=88, rx=12, fill=p["indigo"], stroke=p["indigo_light"]),
                  txt(36, y + 33, num, 18, p["gold"], family="Georgia, Times New Roman, serif"),
                  txt(73, y + 33, title, 17, p["cream"], weight=700),
                  txt(36, y + 65, sub, 16, p["muted"])])
    return svg(420, 365, "Beyond the lab", "Swimming, photography, art, and TFPS leadership", a)


def replace_block(readme, marker, body):
    start, end = f"<!-- {marker}:START -->", f"<!-- {marker}:END -->"
    if readme.count(start) != 1 or readme.count(end) != 1:
        raise ValueError(f"Expected one pair of {marker} markers")
    before, rest = readme.split(start, 1)
    _, after = rest.split(end, 1)
    return before + start + "\n" + body.rstrip() + "\n" + end + after


def project_block(projects):
    parts = ['<p align="center">']
    for project in projects:
        alt = project["name"] + ": " + project["result"] + "; " + project["footnote"]
        parts.append(f'<a href="{escape(project["url"], quote=True)}"><img src="./assets/koi-lab/{project["id"]}.svg" width="420" alt="{escape(alt, quote=True)}" /></a>')
    parts.append('</p>')
    return "\n".join(parts)


def research_block(items):
    return "\n".join(f'- **{item["topic"]}:** {item["detail"]}.' for item in items)


def main():
    c = json.loads((ROOT / "scripts/profile_content.json").read_text(encoding="utf-8"))
    ASSETS.mkdir(exist_ok=True)
    outputs = {"banner.svg": banner(c), "banner-mobile.svg": banner_mobile(c),
               "experience.svg": timeline(c), "experience-mobile.svg": timeline_mobile(c),
               "achievements.svg": achievements(c), "achievements-mobile.svg": achievements_mobile(c)}
    outputs.update({p["id"] + ".svg": card(p, c["palette"]) for p in c["projects"]})
    for name, content in outputs.items():
        (ASSETS / name).write_text(content, encoding="utf-8")
    path = ROOT / "README.md"
    readme = path.read_text(encoding="utf-8")
    readme = replace_block(readme, "PROJECT_CARDS", project_block(c["projects"]))
    readme = replace_block(readme, "CURRENTLY_EXPLORING", research_block(c["currently_exploring"]))
    path.write_text(readme, encoding="utf-8")
    print(f"Rendered {len(outputs)} SVGs and two README blocks")


if __name__ == "__main__":
    main()
